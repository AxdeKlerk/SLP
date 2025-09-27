from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path("checkout/", views.checkout, name="payment_checkout"),
    path("process-payment/", views.process_payment, name="payments_process"),
    path("test-connection/", views.test_square_connection, name="test_square_connection"),
]
