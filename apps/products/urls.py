# apps/products/urls.py
from django.urls import path
from . import views
from apps.products.views import ArtistDetailView, VenueDetailView, get_artist_id, get_venue_id, MerchListView, MerchDetailView

app_name = 'products'

urlpatterns = [
    # Event views
    path('events/', views.events_view, name='events'),
    path('previous-gigs/', views.previous_events_view, name='previous_events'),
    path('roxoff/', views.roxoff_view, name='roxoff'),
    # Detail views for clicking into one artist or venue
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('venue/<int:pk>/', views.VenueDetailView.as_view(), name='venue_detail'),
    # Search views for artist, venue and merch
    path("api/artist-id/", get_artist_id, name="get_artist_id"),
    path("api/venue-id/", get_venue_id, name="get_venue_id"),
    path("api/merch-id/", views.get_merch_id, name="get_merch_id"),
    # Merch CRUD views
    path("merch/", MerchListView.as_view(), name="merch_list"),
    path("merch/<int:pk>/", MerchDetailView.as_view(), name="merch_detail"),
]
