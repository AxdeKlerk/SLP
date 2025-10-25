import json
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from .utils import client
from apps.checkout.models import Order
from apps.user.models import UserProfile
from .models import Invoice
from apps.basket.views import calculate_fees
from apps.checkout.views import prepare_order_context


logger = logging.getLogger(__name__)


@login_required
def payment_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status="pending")
    
    from django.conf import settings

    # Get basket totals and update order
    base_context, subtotal, basket_total = prepare_order_context(order)
    order.subtotal = subtotal
    order.total = basket_total
    order.save()

    # Pre-fill from profile if available
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    initial_data = {}
    if profile:
        initial_data = {
            "shipping_name": profile.full_name,
            "shipping_address": profile.address,
            "shipping_city": profile.city,
            "shipping_postcode": profile.postcode,
            "shipping_country": profile.country,
        }

    # Build final context for template
    context = {
        **base_context,  # merge whatever prepare_order_context returned
        "order": order,
        "initial": initial_data,
        "previous_page": request.META.get("HTTP_REFERER", "/"),
        "SQUARE_APPLICATION_ID": settings.SQUARE_APPLICATION_ID,
        "SQUARE_LOCATION_ID": settings.SQUARE_LOCATION_ID,
    }

    return render(request, "payments/payment.html", context)


def test_square_connection(request):
    result = client.locations.list()
    if hasattr(result, "errors") and result.errors:
        return JsonResponse({"errors": [e.detail for e in result.errors]})

    locations = [loc.dict() for loc in result.locations] if result.locations else []
    return JsonResponse({"locations": locations})


def sandbox_checkout(request):

    from django.conf import settings

    ctx = {
        "SQUARE_APPLICATION_ID": settings.SQUARE_APPLICATION_ID,
        "SQUARE_LOCATION_ID": settings.SQUARE_LOCATION_ID,
    }
    return render(request, "payments/payment.html", ctx)


@login_required
def process_payment(request, order_id):
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

        # Send email confirmation
        from django.core.mail import send_mail
        subject = f"Your Searchlight Promotions Order #{order.id} Confirmation"
        message = (
            f"Hi {order.shipping_name},\n\n"
            f"Thank you for your order!\n\n"
            f"Order Summary:\n"
            f"- Order ID: {order.id}\n"
            f"- Total Paid: £{order.total}\n\n"
            "Your order has been successfully processed. "
            "We'll send another email when your tickets or merchandise are on their way.\n\n"
            "Rock on,\n"
            "The Searchlight Promotions Team"
        )
        send_mail(
            subject,
            message,
            None,  # Uses DEFAULT_FROM_EMAIL
            [order.email],
            fail_silently=False,
        )

        return JsonResponse({"ok": True, "order_id": order.id, "message": "Payment and invoice processed successfully"})

    return JsonResponse({"ok": False, "error": "Invalid request method"}, status=400)


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Update user profile with latest shipping info
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.full_name = getattr(order, "shipping_name", "") or profile.full_name
    profile.address = getattr(order, "shipping_address", "") or profile.address
    profile.city = getattr(order, "shipping_city", "") or profile.city
    profile.postcode = getattr(order, "shipping_postcode", "") or profile.postcode
    profile.country = getattr(order, "shipping_country", "UK")
    profile.save()

    return render(request, "checkout/confirmation.html", {"order": order})
