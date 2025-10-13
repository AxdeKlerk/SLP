from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("basket-checkout/", views.basket_checkout, name="basket_checkout"),
    path("confirmation/<int:order_id>/", views.confirmation_view, name="confirmation"),
    path("checkout/<int:order_id>/", views.checkout_view, name="checkout_view"),
    path("webhooks/square/", views.square_webhook, name="square_webhook"),
]
