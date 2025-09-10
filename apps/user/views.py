from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


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
            return redirect("login")  # after signup, go to login page
    else:
        form = UserCreationForm()
    return render(request, "user/signup.html", {"form": form})

