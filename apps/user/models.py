from django.db import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile(request):
    current_orders = Order.objects.filter(user=request.user).exclude(status="complete")
    past_orders = Order.objects.filter(user=request.user, status="complete")

    return render(request, "user/profile.html", {
        "current_orders": current_orders,
        "past_orders": past_orders,
    })
