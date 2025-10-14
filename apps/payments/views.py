import json
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.conf import settings
from .utils import client
from apps.checkout.models import Order

logger = logging.getLogger(__name__)

def test_square_connection(request):
    result = client.locations.list()
    if hasattr(result, "errors") and result.errors:
        return JsonResponse({"errors": [e.detail for e in result.errors]})

    locations = [loc.dict() for loc in result.locations] if result.locations else []
    return JsonResponse({"locations": locations})

def sandbox_checkout(request):
    print(">>> checkout view hit, App ID =", settings.SQUARE_APPLICATION_ID,
          "Location ID =", settings.SQUARE_LOCATION_ID)  # debug
    ctx = {
        "SQUARE_APPLICATION_ID": settings.SQUARE_APPLICATION_ID,
        "SQUARE_LOCATION_ID": settings.SQUARE_LOCATION_ID,
    }
    return render(request, "payments/checkout.html", ctx)

def process_payment(request):
    print(">>> process_payment view hit")  # debug

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data = json.loads(request.body or "{}")
    token = data.get("token")
    amount = data.get("amount")

    if not token:
        return HttpResponseBadRequest("Missing token from Square Web Payments SDK.")

    logger.info("Square token received (no charge yet): %s | amount=%s", token, amount)
    return JsonResponse({"ok": True, "received_token": True})

@login_required
def payment_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status="pending")

    previous_page = request.META.get("HTTP_REFERER", "/checkout/")

    return render(request, "payments/payment.html", {
        "order": order,
        "SQUARE_APPLICATION_ID": settings.SQUARE_APPLICATION_ID,
        "SQUARE_LOCATION_ID": settings.SQUARE_LOCATION_ID,
        "previous_page": previous_page,
    })