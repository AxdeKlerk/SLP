from django.contrib import admin
from .models import Order, OrderItem
import random
import requests
from django.utils import timezone
from django.conf import settings

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

def verify_with_square(modeladmin, request, queryset):

    """Admin action to verify payment status with Square"""
    access_token = settings.SQUARE_ACCESS_TOKEN
    base_url = "https://connect.squareup.com/v2/payments"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # MOCK MODE: Comment this out when testing live with Square
    mock_mode = True
    possible_statuses = ["APPROVED", "COMPLETED", "CANCELED"]

    for order in queryset:
        if not order.square_payment_id:
            continue  # Skip orders with no Square payment ID

        try:
        # Fake response — randomly pick a status for testing    
            if mock_mode:
                fake_status = random.choice(possible_statuses)
                order.payment_status = fake_status
                order.verified_on = timezone.now()
                order.save(update_fields=["payment_status", "verified_on"])
                modeladmin.message_user(request, f"[MOCK] Order {order.id} verified as {fake_status}")
            else:
                # Fetch payment info from Square API
                response = requests.get(f"{base_url}/{order.square_payment_id}", headers=headers)
                data = response.json()

                # Extract status from response
                payment = data.get("payment", {})
                status = payment.get("status", "UNKNOWN")

                # Update order fields
                order.payment_status = status
                order.verified_on = timezone.now()
                order.save(update_fields=["payment_status", "verified_on"])

                modeladmin.message_user(request, f"Order {order.id} verified: {status}")

        except Exception as e:
            modeladmin.message_user(request, f"Error verifying Order {order.id}: {e}", level="error")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    # Added Square + payment tracking fields
    list_display = (
        "id",
        "email",
        "status",
        "payment_status",
        "square_payment_id",
        "total",
        "verified_on",
        "created_at",
    )

    # Allow filtering by both status types
    list_filter = ("status", "payment_status", "created_at")

    # Add search for Square fields too
    search_fields = ("email", "id", "square_payment_id", "square_order_id")

    # Prevent accidental edits of Square IDs and verification time
    readonly_fields = ("created_at",)
    
    ordering = ("-created_at",)

    # Ensures you can edit everything, including square_payment_id (remove all fields for production)
    fields = (
        "email",
        "status",
        "payment_status",
        "square_order_id",
        "square_payment_id",
        "total",
        "verified_on",
    )

    actions = [verify_with_square]
