import json
import hmac, hashlib, base64, os, requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.basket.models import Basket
from apps.checkout.models import Order, OrderItem
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from decimal import Decimal
from apps.basket.views import calculate_fees


SQUARE_SIGNATURE_KEY = os.getenv("SQUARE_SIGNATURE_KEY")

@login_required
def basket_checkout(request):
    # Get this user's basket
    basket = Basket.objects.filter(user=request.user).first()
    basket_items = basket.items.all() if basket else []

    # Validate ticket capacities
    checked_events = set()
    for item in basket_items:
        if item.event and item.event not in checked_events:
            checked_events.add(item.event)

            sold = item.event.tickets_sold
            capacity = item.event.effective_capacity
            remaining = capacity - sold
            requested_quantity = sum(i.quantity for i in basket_items if i.event == item.event)

            if requested_quantity > remaining:
                ticket_word = "ticket" if remaining == 1 else "tickets"
                messages.error(
                    request,
                    f"Not enough tickets available! Only {remaining} {ticket_word} left for {item.event}!"
                )
                return redirect("basket:basket_view")

    if not basket_items:
        messages.error(request, "Your basket is empty")
        return redirect("basket:basket_view")

    # Create the pending order
    order = Order.objects.create(
        user=request.user,
        email=getattr(request.user, "email", None),
        status="pending",
        subtotal=0,
        total=0,
    )

    # Calculate totals
    subtotal = Decimal('0.00')

    for item in basket_items:
        booking_fee = Decimal('0.00')
        delivery_fee = Decimal('0.00')
        line_total = item.line_total

        # Event booking fee
        if item.event:
            booking_fee = (item.event.price * Decimal('0.10')).quantize(Decimal('0.01'))

        # Merch delivery fee
        if item.merch:
            base_fee = Decimal('5.00')
            extra_fee = (base_fee * Decimal('0.50')).quantize(Decimal('0.01'))
            delivery_fee = base_fee + (extra_fee * (item.quantity - 1))
            delivery_fee = delivery_fee.quantize(Decimal('0.01'))

        # Total for this item
        subtotal += line_total + (booking_fee * item.quantity) + delivery_fee

        # Create order item
        OrderItem.objects.create(
            order=order,
            event=item.event if item.event else None,
            merch=item.merch if item.merch else None,
            quantity=item.quantity,
            price=(line_total / item.quantity) if item.quantity else 0,
        )

    # --- Update totals ---
    order.subtotal = subtotal
    order.total = subtotal
    order.save()

    # --- Create matching Square Order in Sandbox environment ---
    headers = {
        "Square-Version": "2025-01-01",
        "Authorization": f"Bearer {settings.SQUARE_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    order_payload = {
        "order": {
            "location_id": settings.SQUARE_LOCATION_ID,
            "line_items": [
                {
                    "name": "Checkout Order",
                    "quantity": "1",
                    "base_price_money": {
                        "amount": int(order.total * 100),  # Convert to pennies
                        "currency": "GBP",
                    },
                }
            ],
            "state": "OPEN",
        }
    }

    try:
        # 1️ Create the Square Order
        order_response = requests.post(
            f"{settings.SQUARE_BASE_URL}/v2/orders",
            headers=headers,
            json=order_payload,
        )
        order_data = order_response.json()
        square_order_id = order_data.get("order", {}).get("id")

        if square_order_id:
            order.square_order_id = square_order_id
            order.save()

            # 2️ Create the Square Payment
            payment_payload = {
                "source_id": "cnon:card-nonce-ok",  # Sandbox test card token
                "amount_money": {
                    "amount": int(order.total * 100),
                    "currency": "GBP",
                },
                "idempotency_key": f"order-{order.id}",
                "location_id": settings.SQUARE_LOCATION_ID,
                "order_id": square_order_id,
            }

            payment_response = requests.post(
                f"{settings.SQUARE_BASE_URL}/v2/payments",
                headers=headers,
                json=payment_payload,
            )
            payment_data = payment_response.json()
            square_payment_id = payment_data.get("payment", {}).get("id")

            if square_payment_id:
                order.square_payment_id = square_payment_id
                order.save()
                print(f"Created Square Order {square_order_id} and Payment {square_payment_id}")
            else:
                print("Payment ID not returned by Square Sandbox")

        else:
            print("Failed to create Square Order")

    except Exception as e:
        print(f"Error creating Square order/payment: {e}")

    # --- Clear basket and redirect ---
    basket.items.all().delete()
    return redirect("checkout:checkout_view", order_id=order.id)

@login_required
def restore_basket(request, order_id):
    """
    Rebuilds the user's basket from a pending order so they can continue shopping
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Only rebuild if the order is still pending
    if order.status != "pending":
        messages.error(request, "This order has already been completed and cannot be modified")
        return redirect("basket:basket_view")

    # Get or create the basket
    basket, _ = Basket.objects.get_or_create(user=request.user)

    # Clear any existing items (optional but keeps it tidy)
    basket.items.all().delete()

    # Rebuild items from the order
    for item in order.items.all():
        basket.items.create(
            event=item.event,
            merch=item.merch,
            quantity=item.quantity
        )

    messages.success(request, "Your previous basket has been restored")
    return redirect("basket:basket_view")


def confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "checkout/confirmation.html", {"order": order})


@login_required
def checkout_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status="pending")

    context, _, _ = prepare_order_context(order)
    context["previous_page"] = request.META.get("HTTP_REFERER", "/")

    return render(request, "checkout/checkout.html", context)


def prepare_order_context(order):
    """Recalculate fees and return a consistent context for checkout/payment views."""
    # Force the queryset into a list so attached attributes are preserved
    items = list(order.items.all())
    order_items, subtotal, delivery_charge, basket_total = calculate_fees(items)

    # Make absolutely sure we’re returning the *same* modified list
    context = {
        "order": order,
        "order_items": order_items,  # this list has .total_with_fees attached
        "subtotal": subtotal,
        "delivery_charge": delivery_charge,
        "basket_total": basket_total,
    }

    # For debugging
    for i in order_items:
        print(f"CTX CHECK: {i} | total_with_fees={getattr(i, 'total_with_fees', None)}")

    return context, subtotal, basket_total


@csrf_exempt
@require_POST
def square_webhook(request):
    """
    Handle incoming Square payment webhooks securely.
    """
    # --- 1. Verify Square signature (now re-enabled for production) ---
    signature = request.META.get("HTTP_X_SQUARE_HMACSHA256_SIGNATURE", "")
    body = request.body.decode("utf-8")
    key = settings.SQUARE_SIGNATURE_KEY.encode("utf-8")

    # Ensure URL matches exactly to Square dashboard settings
    webhook_url = request.build_absolute_uri().replace("http://", "https://")
    string_to_sign = webhook_url + body

    computed_signature = base64.b64encode(
        hmac.new(key, string_to_sign.encode("utf-8"), hashlib.sha256).digest()
    ).decode("utf-8")

    # Signature verification now active
    if not hmac.compare_digest(computed_signature, signature):
        print("Signature mismatch")
        return HttpResponseBadRequest("Invalid signature")

    # --- 2. Parse the incoming webhook JSON ---
    try:
        event = json.loads(body)
    except json.JSONDecodeError:
        print("Invalid JSON in webhook payload")
        return HttpResponseBadRequest("Invalid JSON")

    event_type = event.get("type", "")
    print(f"Received Square webhook: {event_type}")

    # --- 3. Only handle payment events ---
    if event_type in ["payment.created", "payment.updated"]:
        try:
            # Extract payment info
            payment = event["data"]["object"]["payment"]
            payment_id = payment.get("id")
            square_order_id = payment.get("order_id")
            payment_status = payment.get("status")

            print(f"Square order ID: {square_order_id}, payment ID: {payment_id}, status: {payment_status}")

            # --- 4. Find the matching local order ---
            try:
                order = Order.objects.get(square_order_id=square_order_id)
            except Order.DoesNotExist:
                print(f"No order found for Square order ID {square_order_id}")
                return JsonResponse({"status": "ignored", "message": "No matching order"}, status=200)

            # --- 5. Update only if payment completed ---
            if payment_status == "COMPLETED":
                if order.status != "paid":
                    order.status = "paid"
                    order.square_payment_id = payment_id
                    order.save()
                    print(f"Order {order.id} marked as PAID")
                    return JsonResponse({"status": "success", "message": "Order updated"}, status=200)
                else:
                    print(f"Order {order.id} already marked as PAID — duplicate webhook ignored")
                    return JsonResponse({"status": "ignored", "message": "Duplicate event"}, status=200)
            else:
                print(f"Payment not completed yet (status: {payment_status})")
                return JsonResponse({"status": "ignored", "message": "Payment not completed"}, status=200)

        # --- 6. Handle missing fields safely ---
        except KeyError as e:
            print(f"Missing key in Square payload: {e}")
            return JsonResponse({"status": "error", "message": f"Missing key: {e}"}, status=400)

        # --- 7. Catch any other unexpected errors ---
        except Exception as e:
            print(f"Unexpected error while processing webhook: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # --- 8. Ignore all other event types ---
    else:
        print(f"Unhandled Square webhook event type: {event_type}")
        return JsonResponse({"status": "ignored", "message": f"Unhandled event: {event_type}"}, status=200)


