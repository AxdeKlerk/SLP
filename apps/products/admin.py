from django.contrib import admin
from .models import Event, Artist, Venue, Merch

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ("artist", "venue", "gig_date", "start_time", "genre", "price", "tickets_sold", "tickets_remaining",)
    list_filter = ("special_event", "gig_date", "venue", "artist", "age", "genre")
    search_fields = ("artist__name", "venue__name", "genre")
    autocomplete_fields = ["artist", "supporting_artists"]
    filter_horizontal = ('supporting_artists',)

    def tickets_remaining(self, obj):
        # Safely handle missing or null capacity
        if obj.capacity:
            return obj.capacity - obj.tickets_sold
        return "N/A"
    tickets_remaining.short_description = "Remaining"


class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name']


class VenueAdmin(admin.ModelAdmin):
    search_fields = ['name']


class MerchAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price", "stock", "items_sold", "stock_remaining")
    search_fields = ["product_name"]

    def stock_remaining(self, obj):
        if hasattr(obj, "stock"):
            return max(obj.stock - obj.items_sold, 0)
        return "N/A"
    stock_remaining.short_description = "Remaining"


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Venue)
admin.site.register(Event, EventAdmin)
admin.site.register(Merch)