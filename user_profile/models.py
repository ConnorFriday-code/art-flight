from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    sku = models.CharField(max_length=10, unique=True)
    artist_name = models.CharField(max_length=255, blank=True)  # Will be automatically set to the user's name
    email = models.EmailField(blank=True)  # Hidden, automatically grabbed from the user's profile
    description = models.TextField(blank=True)
    dos = models.TextField(blank=True)
    donts = models.TextField(blank=True)
    image = models.ImageField(upload_to='artist_images/', blank=True, null=True)
    price = models.JSONField()  # Dictionary for up to 5 options and prices
    slots = models.IntegerField(default=0)  # Number of open slots
    tag = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artists')  # Tie artist to user

    def save(self, *args, **kwargs):
        if not self.artist_name:
            self.artist_name = self.user.username  # Automatically set artist name to user's name
        if not self.email:
            self.email = self.user.email  # Automatically set email to user's email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.artist_name