from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from apps.user.forms import ForgotUsernameForm
from apps.checkout.models import Order


@login_required
def login_success_view(request):
    return render(request, "user/login_success.html")

@login_required
def profile_view(request):
    current_orders = Order.objects.filter(user=request.user, status="pending")
    past_orders = Order.objects.filter(user=request.user, status="paid")

    context = {
        "current_orders": current_orders,
        "past_orders": past_orders,
        "page_title": "Profile"       
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

@login_required
def bulk_order_action(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "pay_single":
            order_id = request.POST.get("order_id")
            if order_id:
                request.session["order_ids_to_pay"] = [order_id]
                return redirect("payments:payment_checkout", order_id=order_id)

        elif action == "delete":
            order_ids = request.POST.getlist("order_ids")
            if not order_ids:
                messages.error(request, "No orders selected")
            else:
                # Make sure IDs are integers
                order_ids = [int(i) for i in order_ids if i.isdigit()]
                Order.objects.filter(id__in=order_ids, user=request.user).delete()
                messages.success(request, f"{len(order_ids)} order(s) deleted", extra_tags="orders")
            return redirect("user:profile_view")

    return redirect("user:profile_view")


