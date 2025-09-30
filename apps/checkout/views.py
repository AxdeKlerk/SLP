import json
import hmac, hashlib, base64, os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.basket.models import Basket
from apps.checkout.models import Order, OrderItem
from django.http import HttpResponse, HttpResponseBadRequest
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
    try:
        # Grab headers
        signature_header = request.headers.get("X-Square-Hmacsha256-Signature")
        print("=== Square Webhook Debug ===")
        print("Header SHA256:", signature_header)
        print("Header SHA1:", request.headers.get("X-Square-Signature"))
        print("Body length:", len(request.body))
        print("Loaded SQUARE_SIGNATURE_KEY:", bool(getattr(settings, "SQUARE_SIGNATURE_KEY", None)))

        # Build the string to sign: notification URL + request body
        notification_url = f"https://{request.get_host()}{request.path}"
        print("Notification URL:", notification_url)

        string_to_sign = notification_url + request.body.decode("utf-8")

        # Compute HMAC-SHA256
        secret = settings.SQUARE_SIGNATURE_KEY.encode("utf-8")
        digest = hmac.new(secret, string_to_sign.encode("utf-8"), hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode("utf-8")
        print("Computed signature:", expected)

        # Compare with header
        if not hmac.compare_digest(expected, signature_header or ""):
            print("Computed signature did not match header.")
            return HttpResponseBadRequest("Invalid signature")

        # Parse and log event if signature matches
        data = json.loads(request.body)
        print("Webhook Event Type:", data.get("type"))

        return HttpResponse("Webhook verified and received", status=200)

    except Exception as e:
        print("Webhook error:", str(e))
        return HttpResponseBadRequest("Bad Request")

# Note: You will need to implement actual webhook handling logic here
# based on Square's documentation and your application's requirements.