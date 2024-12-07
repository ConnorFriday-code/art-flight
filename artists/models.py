from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Artist(models.Model):
    tag = models.ForeignKey('Tag', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    artist_name = models.CharField(max_length=254)
    description = models.TextField()
    dos = models.TextField(null=True, blank=True)
    donts = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.artist_name