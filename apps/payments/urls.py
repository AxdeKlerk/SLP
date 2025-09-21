from django.urls import path
from . import views

urlpatterns = [
    path("test-square/", views.test_square, name="test_square"),
]
