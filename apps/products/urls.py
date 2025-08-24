# apps/products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('events/', views.about_view, name='events'),
    path('merch/', views.contact_view, name='merch'),
]