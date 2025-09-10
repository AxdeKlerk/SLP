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
from django.db.models import Q

def events_view(request):
    today = timezone.now().date()  # get today's date
    events = Event.objects.filter(gig_date__gte=today).exclude(event_type='roxoff').order_by('gig_date')
    for e in events:
        e.is_upcoming = e.gig_date >= today
    return render(request, 'events.html', {'events': events, 'page_title': 'Upcoming Events'})

def previous_events_view(request):
    today = timezone.now().date()
    past_events = Event.objects.filter(gig_date__lt=today).order_by('-gig_date')
    for e in past_events:
        e.is_upcoming = False
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

def get_merch_id(request):
    name = request.GET.get("name", "").strip()
    if not name:
        return JsonResponse({"ids": [], "count": 0})

    # Map label -> key for category matches
    choices = Merch._meta.get_field("product_category").choices
    label_keys = [key for key, label in choices if name.lower() in str(label).lower()]

    merch_qs = Merch.objects.filter(
        Q(product_name__icontains=name) |
        Q(product_category__icontains=name) |
        Q(product_category__in=label_keys)
    ).order_by("product_name")

    ids = list(merch_qs.values_list("id", flat=True))
    return JsonResponse({"ids": ids, "count": len(ids)})

class MerchListView(ListView):
    model = Merch
    template_name = "merch.html"
    context_object_name = "items"
    paginate_by = 4

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

def search_view(request):
    category = (request.GET.get("category") or "").strip()
    q = (request.GET.get("q") or "").strip()

    ctx = {"category": category, "q": q}

    if not category or not q:
        return render(request, "search_results.html", ctx)

    if category == "artist":
        ctx["artist_results"] = Artist.objects.filter(
            name__icontains=q
        ).order_by("name")

    elif category == "venue":
        ctx["venue_results"] = Venue.objects.filter(
            name__icontains=q
        ).order_by("name")

    elif category == "merch":
        # Map label -> key for category matches
        choices = Merch._meta.get_field("product_category").choices  # [(key, "Label")]
        label_keys = [key for key, label in choices if q.lower() in str(label).lower()]

        ctx["merch_results"] = Merch.objects.filter(
            Q(product_name__icontains=q) |               # name contains
            Q(product_category__icontains=q) |           # key contains (e.g. "hoodie")
            Q(product_category__in=label_keys)           # label match (e.g. "Hoodie")
        ).order_by("product_name", "product_category", "size")

    return render(request, "search_results.html", ctx)
