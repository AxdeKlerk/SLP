# apps/products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('events/', views.events_view, name='events'),
    path('merch/', views.merch_view, name='merch'),
    # For the artist detail view
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist'),
    # For the venue detail view
    path('venue/<int:pk>/', views.VenueDetailView.as_view(), name='venue'),
]