from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Event(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gig_reviews", null=True, blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    artist = models.ForeignKey("Artist",on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    description = models.TextField(max_length=2000, null=False, blank=False)
    venue = models.ForeignKey("Venue",on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    gig_date = models.DateField(null=False, blank=False)
    door_time = models.TimeField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
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
    age = models.CharField(max_length=10, choices=AGE_CHOICES, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
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

    class Meta:
        ordering = ['name']
    def __str__(self):
        return f"{self.name}"