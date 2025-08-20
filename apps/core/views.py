from django.shortcuts import render
from django.views import View


# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def thankyou_view(request):
    return render(request, 'thankyou.html')

# Testing 500 page
def crash_view(request):
    # This will crash on purpose
    1 / 0

#Testing 404 page
from django.shortcuts import render

def test_404_template(request):
    return render(request, '404.html')
