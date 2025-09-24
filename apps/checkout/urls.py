from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("", views.order_review, name="order_review"),
    path("confirmation/<int:order_id>/", views.confirmation_view, name="confirmation"),
]
