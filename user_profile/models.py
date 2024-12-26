from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Artist(models.Model):
    sku = models.CharField(max_length=10, unique=True)
    artist_name = models.CharField(max_length=255, editable=False)
    email = models.EmailField(editable=False)
    description = models.TextField(blank=True)
    dos = models.TextField(blank=True)
    donts = models.TextField(blank=True)
    image = models.ImageField(upload_to='artist_images/', blank=True, null=True)
    price_options = models.JSONField(default=dict)
    slots = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50)])
    tag = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artists')

    def save(self, *args, **kwargs):
        """Automatically populate artist_name and email from user on save."""
        if self.user:
            self.artist_name = self.user.username
            self.email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.artist_name