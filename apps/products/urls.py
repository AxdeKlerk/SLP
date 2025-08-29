# apps/products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('events/', views.events_view, name='events'),
    path('previous-gigs/', views.previous_events_view, name='previous_events'),
    #path('artist/', views.artist_view, name='artist'),
    #path('venue/', views.venue_view, name='venue'),
    path('roxoff/', views.roxoff_view, name='roxoff'),
    path('merch/', views.merch_view, name='merch'),
    # Detail views for clicking into one artist or venue
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('venue/<int:pk>/', views.VenueDetailView.as_view(), name='venue_detail'),
]
