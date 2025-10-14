import json
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.conf import settings
from .utils import client
from apps.checkout.models import Order
from .models import Invoice

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

@login_required
def process_payment(request):
    """
    Handles Square payment confirmation and creates/updates
    an invoice record for the associated order.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        token = data.get("token")
        amount = data.get("amount")
        address = data.get("addressData", {})
        invoice = data.get("invoiceData", {})
        use_same_address = invoice.get("useSameAddress", True)

        # Get the user's pending order
        order = Order.objects.filter(user=request.user, status="pending").last()
        if not order:
            return JsonResponse({"ok": False, "error": "No pending order found."}, status=404)

        order.status = "paid"
        order.save()

        # Create or update invoice record
        invoice_obj, created = Invoice.objects.get_or_create(order=order)
        invoice_obj.use_same_address = use_same_address

        if not use_same_address:
            invoice_obj.invoice_name = invoice.get("name")
            invoice_obj.invoice_company = invoice.get("company")
            invoice_obj.invoice_email = invoice.get("email")
            invoice_obj.invoice_address = invoice.get("address")
            invoice_obj.invoice_city = invoice.get("city")
            invoice_obj.invoice_postcode = invoice.get("postcode")
            invoice_obj.invoice_country = invoice.get("country", "UK")
        else:
            # copy details from the order’s shipping info
            invoice_obj.invoice_name = order.shipping_name
            invoice_obj.invoice_email = order.email
            invoice_obj.invoice_address = order.shipping_address
            invoice_obj.invoice_city = order.shipping_city
            invoice_obj.invoice_postcode = order.shipping_postcode
            invoice_obj.invoice_country = order.shipping_country

        invoice_obj.save()

        return JsonResponse({"ok": True, "message": "Payment and invoice processed successfully."})

    return JsonResponse({"ok": False, "error": "Invalid request method."}, status=400)

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