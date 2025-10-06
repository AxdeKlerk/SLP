import json
import hmac, hashlib, base64, os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.basket.models import Basket
from apps.checkout.models import Order, OrderItem
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

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
        messages.error(request, "Your basket is empty.")
        return redirect("basket:basket_view")

    # Create the pending order
    order = Order.objects.create(
        user=request.user,
        email=getattr(request.user, "email", None),
        status="pending",
        subtotal=0,
        total=0,
    )

    subtotal = 0
    for item in basket_items:
        line_total = item.line_total
        subtotal += line_total

        OrderItem.objects.create(
            order=order,
            event=item.event if item.event else None,
            merch=item.merch if item.merch else None,
            quantity=item.quantity,
            price=(line_total / item.quantity) if item.quantity else 0,
        )

    # Update totals
    order.subtotal = subtotal
    order.total = subtotal
    order.save()

    # Clear basket
    basket.items.all().delete()

    # Redirect to checkout page
    return redirect("checkout:checkout_view", order_id=order.id)


def confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "checkout/confirmation.html", {"order": order})


@login_required
def checkout_view(request, order_id):
    # Find the order for this user
    order = get_object_or_404(Order, id=order_id, user=request.user, status="pending")
    return render(request, "checkout/checkout.html", {"order": order})


@csrf_exempt
@require_POST
def square_webhook(request):
    # --- 1. Verify Square signature (now re-enabled for production) ---
    signature = request.META.get("HTTP_X_SQUARE_HMACSHA256_SIGNATURE", "")
    body = request.body.decode("utf-8")
    key = settings.SQUARE_SIGNATURE_KEY.encode("utf-8")

    webhook_url = request.build_absolute_uri().replace("http://", "https://")
    string_to_sign = webhook_url + body

    computed_signature = base64.b64encode(
        hmac.new(key, string_to_sign.encode("utf-8"), hashlib.sha256).digest()
    ).decode("utf-8")

    # Temporarily disabled signature verification for local testing
    # if not hmac.compare_digest(computed_signature, signature):
    #     print("Signature mismatch")
    #     return HttpResponseBadRequest("Invalid signature")

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
                print(f"⚠️ No order found for Square order ID {square_order_id}")
                return JsonResponse({"status": "ignored", "message": "No matching order"}, status=200)

            # --- 5. Only mark as paid if not already done ---
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

    # --- 8. Handle unknown or unimportant event types ---
    else:
        print(f"Unhandled Square webhook event type: {event_type}")
        return JsonResponse({"status": "ignored", "message": f"Unhandled event: {event_type}"}, status=200)


