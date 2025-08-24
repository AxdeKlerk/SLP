from django.contrib import admin
from .models import Event, Artist, Venue

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("artist", "venue", "gig_date", "start_time", "genre", "price")
    list_filter = ("gig_date", "venue", "artist", "age", "genre")
    search_fields = ("artist__name", "venue__name", "genre")

admin.site.register(Artist)
admin.site.register(Venue)
