from django.shortcuts import render
from django.views import View


def home_view(request):
    return render(request, 'core/home.html', {'page_title': 'Home'})


def about_view(request):
    return render(request, 'core/about.html', {'page_title': 'About'})


def contact_view(request):
    return render(request, 'core/contact.html', {'page_title': 'Contact'})


def thankyou_view(request):
    return render(request, 'core/thankyou.html')


