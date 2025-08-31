from django.contrib import admin
from .models import Event, Artist, Venue, Merch

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ("artist", "venue", "gig_date", "start_time", "genre", "price")
    list_filter = ("special_event", "gig_date", "venue", "artist", "age", "genre")
    search_fields = ("artist__name", "venue__name", "genre")
    autocomplete_fields = ["artist", "supporting_artists"]
    filter_horizontal = ('supporting_artists',)

class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name']

class VenueAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Venue)
admin.site.register(Event, EventAdmin)
admin.site.register(Merch)