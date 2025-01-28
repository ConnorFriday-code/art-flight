from django.db import models
from django.contrib.auth.models import User
import uuid

class Artist(models.Model):
    sku = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    artist_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    dos = models.TextField(blank=True)
    donts = models.TextField(blank=True)
    image = models.ImageField(upload_to='artist_images/', blank=True, null=True)
    price = models.JSONField(default=dict, null=False, blank=False)
    slots = models.IntegerField(default=0)
    tag = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artists')

    def save(self, *args, **kwargs):
        if not self.artist_name:
            self.artist_name = self.user.username
        if not self.email:
            self.email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.artist_name