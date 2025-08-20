# apps/core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('thankyou/', views.thankyou_view, name='thankyou'),
    path('crash/', views.crash_view, name='crash'), #for testing 500 page
    path('test404/', views.test_404_template), #for testing 404 page
]
