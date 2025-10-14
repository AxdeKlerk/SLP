from django.db import models
from apps.checkout.models import Order


class Invoice(models.Model):
    """
    Stores invoice details linked to a specific order
    Each order can have one invoice record — either using
    the same address as shipping or a separate one for billing
    """

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="invoice",
        help_text="The order this invoice belongs to"
    )

    # Toggle for using the same address or not
    use_same_address = models.BooleanField(
        default=True,
        help_text="Check if invoice uses the same address as the order's shipping details"
    )

    # Invoice contact/company info
    invoice_name = models.CharField(max_length=100, blank=True, null=True)
    invoice_company = models.CharField(max_length=150, blank=True, null=True)
    invoice_email = models.EmailField(blank=True, null=True)

    # Invoice address
    invoice_address = models.TextField(blank=True, null=True)
    invoice_city = models.CharField(max_length=100, blank=True, null=True)
    invoice_postcode = models.CharField(max_length=20, blank=True, null=True)
    invoice_country = models.CharField(
        max_length=100,
        default="UK",
        blank=True,
        null=True,
        help_text="Defaults to UK if not specified"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        status = "Same as shipping" if self.use_same_address else "Different address"
        return f"Invoice for Order #{self.order.id} ({status})"

