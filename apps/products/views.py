from django.utils import timezone
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.http import JsonResponse
from .models import Event, Artist, Venue

def events_view(request):
    today = timezone.now().date()  # get today's date
    events = Event.objects.filter(gig_date__gte=today).exclude(event_type='roxoff').order_by('gig_date')
    return render(request, 'events.html', {'events': events})

def previous_events_view(request):
    today = timezone.now().date()
    past_events = Event.objects.filter(gig_date__lt=today).order_by('-gig_date')
    return render(request, 'previous_events.html', {'events': past_events})

def merch_view(request):
    return render(request, 'merch.html')

def roxoff_view(request):
    roxoff_event = Event.objects.filter(special_event=True).order_by('gig_date')
    return render(request, 'roxoff.html', {'events': roxoff_event})

class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'artist.html' 
    context_object_name = 'artist'

class VenueDetailView(DetailView):
    model = Venue
    template_name = 'venue.html' 
    context_object_name = 'venue'

def get_artist_id(request):
    name = request.GET.get("name", "")
    artist = Artist.objects.filter(name__icontains=name.strip()).first()
    return JsonResponse({"id": artist.pk if artist else None})

def get_venue_id(request):
    name = request.GET.get("name", "")
    venue = Venue.objects.filter(name__icontains=name.strip()).first()
    return JsonResponse({"id": venue.pk if venue else None})
