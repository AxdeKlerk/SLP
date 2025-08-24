from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from .models import Event, Artist, Venue

# Create your views here.
def events_view(request):
    return render(request, 'events.html')

def merch_view(request):
    return render(request, 'merch.html')

class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'artist.html' 
    context_object_name = 'artist'

class VenueDetailView(DetailView):
    model = Venue
    template_name = 'venue.html' 
    context_object_name = 'venue'