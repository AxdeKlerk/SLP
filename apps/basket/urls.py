# apps/basket/urls.py
from django.urls import path
from . import views

app_name = "basket"

urlpatterns = [
    path('', views.basket_view, name='basket_view'),
    path('add/<int:event_id>/', views.add_to_basket, name='add_to_basket'),
]