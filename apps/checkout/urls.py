from django.urls import path
from . import views
from apps.checkout.views import confirmation_view, basket_checkout

app_name = "checkout"

urlpatterns = [
    path("checkout/", views.basket_checkout, name="basket_checkout"),
    path("confirmation/<int:order_id>/", views.confirmation_view, name="confirmation"),
    path("checkout/<int:order_id>/", views.checkout_view, name="checkout_view"),

]
