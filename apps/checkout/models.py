from django.db import models
from django.conf import settings

class Order(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    # Order totals
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Status tracking
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    square_payment_id = models.CharField(max_length=100, blank=True, null=True)
    square_order_id = models.CharField(max_length=100, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    event = models.ForeignKey("products.Event", null=True, blank=True, on_delete=models.CASCADE)
    merch = models.ForeignKey("products.Merch", null=True, blank=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200, blank=True)  
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def save(self, *args, **kwargs):
        if self.event:
            self.product_name = self.event.title or str(self.event)
        elif self.merch:
            self.product_name = self.merch.product_name
        super().save(*args, **kwargs)

    def line_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"

