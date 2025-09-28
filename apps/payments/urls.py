from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path("sandbox-checkout/", views.sandbox_checkout, name="sandbox_checkout"),
    path("process-payment/", views.process_payment, name="payments_process"),
    path("test-connection/", views.test_square_connection, name="test_square_connection"),
    path("payment/<int:order_id>/", views.payment_checkout, name="payment_checkout"),
]
