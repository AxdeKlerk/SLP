from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm


def home_view(request):
    return render(request, 'core/home.html', {'page_title': 'Home'})


def about_view(request):
    return render(request, 'core/about.html', {'page_title': 'About'})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            first = form.cleaned_data["first_name"]
            last = form.cleaned_data["last_name"]
            sender_email = form.cleaned_data["email"]
            phone = form.cleaned_data.get("phone", "Not provided")
            message = form.cleaned_data["message"]

            # Email to site owner (you)
            subject_admin = f"New contact from {first} {last}"
            body_admin = (
                f"Name: {first} {last}\n"
                f"Email: {sender_email}\n"
                f"Phone: {phone}\n\n"
                f"Message:\n{message}"
            )
            send_mail(subject_admin, body_admin, settings.DEFAULT_FROM_EMAIL, [settings.EMAIL_HOST_USER])

            # Confirmation email to sender
            subject_user = "Thanks for contacting Searchlight Promotions!"
            body_user = (
                f"Hi {first},\n\n"
                "Thanks for getting in touch with Searchlight Promotions.\n"
                "We've received your message and will get back to you soon.\n\n"
                "Best,\n"
                "The Searchlight Promotions Team"
            )
            send_mail(subject_user, body_user, settings.DEFAULT_FROM_EMAIL, [sender_email])

            # Redirect to thank-you page
            return redirect("core:thankyou")
            
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {"form": form, "page_title": "Contact"})


def thankyou_view(request):
    return render(request, 'core/thankyou.html')


