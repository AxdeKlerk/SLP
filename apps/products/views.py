from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from .models import Event, Artist, Venue, Merch
from .forms import MerchForm
from django.urls import reverse_lazy

def events_view(request):
    today = timezone.now().date()  # get today's date
    events = Event.objects.filter(gig_date__gte=today).exclude(event_type='roxoff').order_by('gig_date')
    return render(request, 'events.html', {'events': events, 'page_title': 'Upcoming Events'})

def previous_events_view(request):
    today = timezone.now().date()
    past_events = Event.objects.filter(gig_date__lt=today).order_by('-gig_date')
    return render(request, 'previous_events.html', {'events': past_events, 'page_title': 'Previous Events'})

def merch_view(request):
    return render(request, 'merch.html', {'page_title': 'Merch'})

def roxoff_view(request):
    roxoff_event = Event.objects.filter(special_event=True).order_by('gig_date')
    return render(request, 'roxoff.html', {'events': roxoff_event})

class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'artist.html' 
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Artist"
        return context

class VenueDetailView(DetailView):
    model = Venue
    template_name = 'venue.html' 
    context_object_name = 'venue'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Venue"
        return context

def get_artist_id(request):
    name = request.GET.get("name", "")
    artist = Artist.objects.filter(name__icontains=name.strip()).first()
    return JsonResponse({"id": artist.pk if artist else None})

def get_venue_id(request):
    name = request.GET.get("name", "")
    venue = Venue.objects.filter(name__icontains=name.strip()).first()
    return JsonResponse({"id": venue.pk if venue else None})

class MerchListView(ListView):
    model = Merch
    template_name = "merch.html"
    context_object_name = "items"
    paginate_by = 12  # easy grid pages

    def get_queryset(self):
        qs = super().get_queryset().order_by("product_name")
        q = self.request.GET.get("q")
        cat = self.request.GET.get("category")
        if q:
            qs = qs.filter(product_name__icontains=q)
        if cat:
            qs = qs.filter(product_category=cat)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Merch"
        return context

class MerchDetailView(DetailView):
    model = Merch
    template_name = "merch.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Merch"
        context['size_choices'] = Merch._meta.get_field("size").choices
        return context

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self): return self.get_object().created_by == self.request.user

# Logged In only (CRUD)
class MerchCreateView(CreateView):
    model = Merch
    form_class = MerchForm
    template_name = "merch.html"
    success_url = reverse_lazy("products:merch_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Merch"
        return context

class MerchUpdateView(UpdateView):
    model = Merch
    form_class = MerchForm
    template_name = "merch.html"
    success_url = reverse_lazy("products:merch_list")

    def form_valid(self, form):
        messages.success(self.request, "Merch item updated")
        return super().form_valid(form)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Merch"
        return context

class MerchDeleteView(DeleteView):
    model = Merch
    template_name = "merch.html"
    success_url = reverse_lazy("products:merch_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Item deleted.")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Merch"
        return context

