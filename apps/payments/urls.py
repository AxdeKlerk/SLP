from django.urls import path
from . import views

urlpatterns = [
    path("test-square/", views.test_square, name="test_square"),
    path("test-connection/", views.test_square_connection, name="test_square_connection"),
]
