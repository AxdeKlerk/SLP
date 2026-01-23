import json
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .utils import client
from apps.checkout.models import Order
from apps.user.models import UserProfile
from .models import Invoice
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
        **base_context,
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
    if request.method != "POST":
        return JsonResponse(
            {"ok": False, "error": "Invalid request method"},
            status=400
        )

    data = json.loads(request.body)
    invoice = data.get("invoiceData", {})
    use_same_address = invoice.get("useSameAddress", True)

    # Get the user's pending order
    order = Order.objects.filter(
        user=request.user, status="pending").last()
    if not order:
        return JsonResponse(
            {"ok": False, "error": "No pending order found."},
            status=404
        )

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
        invoice_obj.invoice_name = order.shipping_name
        invoice_obj.invoice_email = order.email
        invoice_obj.invoice_address = order.shipping_address
        invoice_obj.invoice_city = order.shipping_city
        invoice_obj.invoice_postcode = order.shipping_postcode
        invoice_obj.invoice_country = order.shipping_country

    invoice_obj.save()

    # Try sending confirmation email
    from django.core.mail import send_mail
    try:
        # Determine the best name for email greeting
        name = (
            order.shipping_name
            or request.user.get_full_name()
            or request.user.username
            or "there"
        )
        subject = f"Your Searchlight Promotions Order #{order.id} Confirmation"
        message = (
            f"Hi {name},\n\n"
            f"Thank you for your order!\n\n"
            f"Order Summary:\n"
            f"- Order ID: {order.id}\n"
            f"- Total Paid: £{order.total}\n\n"
            "Your order has been successfully processed. "
            "We'll send another email when your tickets or merchandise are "
            "on their way.\n\n"
            "Stay Loud!\n"
            "The Searchlight Promotions Team"
        )
        send_mail(subject, message, None, [order.email], fail_silently=False)
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        # Payment succeeded but email failed — log but don't block success
        return JsonResponse({
            "ok": True,
            "order_id": order.id,
            "warning": f"Payment succeeded but email failed: {e}"
        })

    return JsonResponse({
        "ok": True,
        "order_id": order.id,
        "message": "Payment and invoice processed successfully"
    })


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
