# apps/products/urls.py
from django.urls import path
from . import views
from apps.products.views import ArtistDetailView, VenueDetailView, get_artist_id, get_venue_id

app_name = 'products'

urlpatterns = [
    path('events/', views.events_view, name='events'),
    path('previous-gigs/', views.previous_events_view, name='previous_events'),
    path('roxoff/', views.roxoff_view, name='roxoff'),
    path('merch/', views.merch_view, name='merch'),
    # Detail views for clicking into one artist or venue
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('venue/<int:pk>/', views.VenueDetailView.as_view(), name='venue_detail'),
    # Search views for artist and venue
    #path("search/artist/<int:pk>/", ArtistDetailView.as_view(), name="artist_detail"),
    #path("search/venue/<int:pk>/", VenueDetailView.as_view(), name="venue_detail"),
    # API endpoints for fetching artist and venue IDs
    path("api/artist-id/", get_artist_id, name="get_artist_id"),
    path("api/venue-id/", get_venue_id, name="get_venue_id"),
]
