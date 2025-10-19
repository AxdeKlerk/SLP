from django.contrib import admin
from .models import Event, Artist, Venue, Merch, MerchVariant
from django.utils.html import format_html, format_html_join

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ("artist", "venue", "gig_date", "start_time", "genre", "price", "tickets_sold", "tickets_remaining",)
    list_filter = ("special_event", "gig_date", "venue", "artist", "age", "genre")
    search_fields = ("artist__name", "venue__name", "genre")
    autocomplete_fields = ["artist", "supporting_artists"]
    filter_horizontal = ('supporting_artists',)

    def tickets_remaining(self, obj):
        # Safely handle missing or null capacity
        if obj.ticket_capacity:
            return obj.ticket_capacity - obj.tickets_sold
        return "N/A"
    tickets_remaining.short_description = "Remaining"


class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name']


class VenueAdmin(admin.ModelAdmin):
    search_fields = ['name']


class MerchVariantInline(admin.TabularInline):
    model = MerchVariant
    extra = 0
    fields = ("size", "stock", "items_sold")
    readonly_fields = ("items_sold", "stock_remaining")

    def items_sold(self, obj):
        # Count how many of this specific variant have been sold
        return OrderItem.objects.filter(variant=obj).count()
    items_sold.short_description = "Items Sold"

    def stock_remaining(self, obj):
        sold = OrderItem.objects.filter(variant=obj).count()
        return obj.stock - sold
    stock_remaining.short_description = "Stock Remaining"

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        readonly.append("stock_remaining")
        return readonly


class MerchAdmin(admin.ModelAdmin):
    list_display = ("product_name", "category_display", "variant_summary")
    search_fields = ["product_name"]

    def category_display(self, obj):
        return obj.get_product_category_display()
    category_display.short_description = "Category"

    def variant_summary(self, obj):
        """Show all variants directly under the merch item"""
        variants = obj.variants.all()
        if not variants:
            return "No variants"

        rows = []
        for v in variants:
            rows.append(
                f"<tr><td>{v.size or '-'}</td>"
                f"<td>{v.stock}</td>"
                f"<td>{v.items_sold}</td>"
                f"<td>{v.stock - v.items_sold}</td></tr>"
            )

        table_html = (
            "<table style='margin-top:5px; border-collapse: collapse;'>"
            "<tr><th>Size</th><th>Stock</th><th>Sold</th><th>Remaining</th></tr>"
            + "".join(rows)
            + "</table>"
        )
        return format_html(table_html)

    variant_summary.short_description = "Variants"


class MerchVariantAdmin(admin.ModelAdmin):
    list_display = ("merch", "size", "stock", "items_sold")

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Venue)
admin.site.register(Event, EventAdmin)
admin.site.register(Merch, MerchAdmin)
admin.site.register(MerchVariant)