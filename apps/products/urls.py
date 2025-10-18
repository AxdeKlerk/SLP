# apps/products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Event views
    path('events/', views.events_view, name='events'),
    path('previous-gigs/', views.previous_events_view, name='previous_events'),
    path('roxoff/', views.roxoff_view, name='roxoff'),
    # Detail views
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('venue/<int:pk>/', views.VenueDetailView.as_view(), name='venue_detail'),
    path("event/<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
    # Search for artist, venue and merch
    path('search-view/', views.search_view, name='search_view'),
    # Merch list and detail
    path("merch/", views.MerchListView.as_view(), name="merch_list"),
    path("merch/<int:pk>/", views.MerchDetailView.as_view(), name="merch_detail"),
]
