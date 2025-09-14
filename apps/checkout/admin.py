from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "email", "status", "created_at", "total")
    list_filter = ("status", "created_at")
    search_fields = ("email", "id")

admin.site.register(Order, OrderAdmin)

