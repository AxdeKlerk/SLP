import json
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.conf import settings
from .utils import client

logger = logging.getLogger(__name__)

def test_square_connection(request):
    result = client.locations.list()
    if hasattr(result, "errors") and result.errors:
        return JsonResponse({"errors": [e.detail for e in result.errors]})

    locations = [loc.dict() for loc in result.locations] if result.locations else []
    return JsonResponse({"locations": locations})

def checkout(request):
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
