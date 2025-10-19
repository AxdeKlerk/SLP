import uuid, requests
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from apps.user.forms import ForgotUsernameForm
from apps.checkout.models import Order
from django.conf import settings
from django.core.paginator import Paginator


@login_required
def login_success_view(request):
    return render(request, "user/login_success.html")

@login_required
def profile(request):
    current_orders = Order.objects.filter(user=request.user).exclude(status="complete")
    past_orders = Order.objects.filter(user=request.user, status="complete")

    return render(request, "user/profile.html", {
        "current_orders": current_orders,
        "past_orders": past_orders,
    })


@login_required
def profile_view(request):
    current_orders = Order.objects.filter(user=request.user, status="pending")
    past_orders = Order.objects.filter(user=request.user, status="paid").order_by('-created_at')

    # Paginate: 4 per page
    paginator = Paginator(past_orders, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "current_orders": current_orders,
        "past_orders": past_orders,
        "page_title": "Profile",
        "previous_page": request.META.get("HTTP_REFERER", "/"),       
    }
    return render(request, "user/profile.html", context)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "user/signup.html", {"form": form})


def forgot_username(request):
    message_sent = True
    if request.method == "POST":
        form = ForgotUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                send_mail(
                    subject="Your Username",
                    message=f"Hi,\n\nYour username is: {user.username}\n\nThanks,\nThe Searchlight Promotions Team",
                    from_email="no-reply@searchlightpromotions.com",
                    recipient_list=[email],
                )
            return redirect ("password_reset_done")
    else:
        form = ForgotUsernameForm()
    return render(
        request,
        "registration/forgot_username.html",
        {"form": form, "message_sent": message_sent},
    )


@require_POST
def bulk_order_action(request):
    order_ids = request.POST.getlist("order_ids")
    action = request.POST.get("action")

    if not order_ids:
        messages.error(request, "No orders selected", extra_tags="orders")
        return redirect("user:profile_view")

    if action == "delete":
        qs = Order.objects.filter(id__in=order_ids, user=request.user, status="pending")
        order_count = qs.count()
        qs.delete()
        messages.success(request, f"{order_count} order(s) deleted", extra_tags="orders")
        return redirect("user:profile_view")

    elif action == "pay_single":
        order_id = order_ids[0]
        order = get_object_or_404(Order, id=order_id, user=request.user, status="pending")

        # Build payment link payload
        idempotency_key = str(uuid.uuid4())
        payload = {
        "idempotency_key": idempotency_key,
        "quick_pay": {
            "name": f"Order #{order.id}",
            "price_money": {
                "amount": int(order.total * 100),
                "currency": "GBP"
            },
            "location_id": settings.SQUARE_LOCATION_ID
        }
    }

    headers = {
        "Square-Version": "2025-09-30",
        "Authorization": f"Bearer {settings.SQUARE_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    print("=== Square Debug ===")
    print("Auth Header:", headers["Authorization"][:20])
    print("Base URL:", settings.SQUARE_BASE_URL)
    print("Location ID:", settings.SQUARE_LOCATION_ID)

    response = requests.post(
        f"{settings.SQUARE_BASE_URL}/v2/online-checkout/payment-links",
        json=payload,
        headers=headers,
        timeout=10,
    )

    print("Status:", response.status_code)
    print("Body:", response.text)

    if response.status_code == 200:
        data = response.json()
        link_url = data["payment_link"]["url"]
        messages.success(request, "Redirecting to payment...", extra_tags="orders")
        return redirect(link_url)
    else:
        messages.error(request, f"Square API error: {response.text}", extra_tags="orders")
        return redirect("user:profile_view")

