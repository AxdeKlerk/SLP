from django.conf import settings
from apps.products.models import Event, Merch
from django.db import models

class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Basket for {self.user}"

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, related_name='items', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_basket_items' , null=True, blank=True)
    merch = models.ForeignKey(Merch, on_delete=models.CASCADE, related_name='merch_basket_items' , null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} × {self.event}"

    @property
    def line_total(self):
        if self.event:
            return (self.event.price or 0) * self.quantity
        if self.merch:
            return (self.merch.price or 0) * self.quantity
        return 0

    def __str__(self):
        if self.event:
            return f"{self.quantity} × {self.event}"
        if self.merch:
            return f"{self.quantity} × {self.merch}"
        return "Basket Item"
    
    class Meta:
        ordering = ["id"]  # keeps insertion order
