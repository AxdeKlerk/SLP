from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("", views.checkout_view, name="checkout"),
    path("confirmation/<int:order_id>/", views.confirmation_view, name="confirmation"),
]
