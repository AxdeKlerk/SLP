from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from apps.user.forms import ForgotUsernameForm


@login_required
def login_success_view(request):
    return render(request, "user/login_success.html")

def profile_view(request):
    return render(request, "user/profile.html", {"page_title": "Profile"})

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
    message_sent = False
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

