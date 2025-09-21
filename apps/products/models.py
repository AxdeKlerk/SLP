from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Event(models.Model):
    image = CloudinaryField('image', folder='slp-upgrade', use_filename=True, blank=True, null=True)
    title = models.CharField(max_length=200, null=True, blank=True, help_text="Optional: Add a title for the event (e.g. Tour Name)")
    artist = models.ForeignKey("Artist",on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    supporting_artists = models.ManyToManyField('Artist', related_name='supporting_for', blank=True, help_text='Select supporting artists from the dropdown')
    description = models.TextField(max_length=2000, null=False, blank=True)
    venue = models.ForeignKey("Venue",on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    gig_date = models.DateField(null=False, blank=False)
    door_time = models.TimeField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    ticket_capacity = models.PositiveIntegerField(default=0)
    GENRE_CHOICES = [
        ('classic_rock', 'Classic Rock'),
        ('rock', 'Rock'),
        ('hard_rock', 'Hard Rock'),
        ('metal', 'Metal'),
        ('heavy_metal', 'Heavy Metal'),
    ]
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='rock')
    AGE_CHOICES = [
        ('All Ages', 'All Ages'),
        ('18+', '18+ only'),
        ('14+', '14+ must be accompanied by an adult'),
    ]
    age = models.CharField(choices=AGE_CHOICES, default='14+ must be accompanied by an adult')
    price = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    special_event = models.BooleanField(default=False)
    EVENT_TYPE_CHOICES = [
        ('regular', 'Regular Event'),
        ('roxoff', 'Roxoff'),
    ]
    event_type = models.CharField(max_length=10,choices=EVENT_TYPE_CHOICES, default='regular')
    ROXOFF_DAY_CHOICES = [
        ('day1', 'Day 1'),
        ('day2', 'Day 2'),
    ]
    roxoff_day = models.CharField(max_length=10,choices=ROXOFF_DAY_CHOICES, blank=True, null=True,help_text="Only required for Roxoff events")
    
    @property
    def tickets_sold(self):
        from apps.checkout.models import OrderItem
        return sum(
            item.quantity
            for item in OrderItem.objects.filter(
                order__status="paid", event=self
            )
        )

    @property
    def effective_capacity(self):
        return min(self.ticket_capacity, self.venue.capacity if self.venue else self.ticket_capacity)

    @property
    def tickets_remaining(self):
        return self.ticket_capacity - self.tickets_sold

    class Meta:
        ordering = ['-gig_date']
    def __str__(self):
        return f"{self.artist} @ {self.venue} | {self.gig_date}"
   
class Artist(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    logo = CloudinaryField('image', blank=True, null=True)
    bio = models.TextField(max_length=2000, null=False, blank=False)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return f"{self.name}"

class Venue(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    logo = CloudinaryField('image', blank=True, null=True)
    bio = models.TextField(max_length=2000, null=False, blank=False)
    website = models.URLField(blank=True)
    capacity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return f"{self.name}"

class Merch(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.TextField(blank=True)
    image = CloudinaryField("image", blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=0, default=0.00)
    CATEGORY_CHOICES = [
        ("tshirt", "T-Shirt"),
        ("hoodie", "Hoodie"),
        ("flag", "Flag"),
        ("cap", "Cap"),
        ("mug", "Mug"),
    ]
    product_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    SIZE_CHOICES = [
        ("xs", "XS"),
        ("s", "S"),
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
        ("xxl", "XXL"),
    ]
    size = models.CharField(
        max_length=5, choices=SIZE_CHOICES, blank=True, null=True,
        help_text="Leave blank for items without sizes (flags, mugs, etc.)."
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Units per product item (keep 1 unless you sell multi-packs)."
    )
    stock = models.PositiveIntegerField(default=0, help_text="How many you have in stock.")

    class Meta:
        ordering = ['product_name'] 
    def __str__(self):
        return f"{self.product_name} - {self.get_product_category_display()} ({self.size if self.size else 'One Size'})"


