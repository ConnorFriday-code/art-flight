import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


# Artist post model
class Artist(models.Model):
    # Random id/sku
    sku = models.CharField(
        max_length=36,
        unique=True,
        default=uuid.uuid4,
    )
    # Artist name
    artist_name = models.CharField(max_length=255, blank=True)
    # Email
    email = models.EmailField(blank=True)
    # Description text field
    description = models.TextField(blank=True)
    # Dos text field
    dos = models.TextField(blank=True)
    # Don'ts text field
    donts = models.TextField(blank=True)
    # Image field (can be blank)
    image = models.ImageField(
        upload_to="artist_images/",
        blank=True,
        null=True,
    )
    # Price field
    price = models.JSONField(default=dict, null=False, blank=False)
    # How many commission slots the artist wants available
    slots = models.IntegerField(default=0)


    # What the user want to tag their art as
    # This works with the nav bar at the top for quick tag/style finding
    class ArtTag(models.TextChoices):
        SKETCH = 'sketch', 'Sketch'
        FLAT = 'flat', 'Flat'
        SHADED = 'shaded', 'Shaded'
        DRAWING = 'drawing', 'Drawing'
        PAINTING = 'painting', 'Painting'
        OIL = 'oil', 'Oil'
        CD = 'cd', 'CD'
        PINS = 'pins', 'Pins'
        MISC = 'misc', 'Miscellaneous'

    tag = models.CharField(
        max_length=20,
        choices=ArtTag.choices,
        blank=True
    )


    # On artist being deleted, delte all posts as well
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="artists",
    )

    # Save checking username
    def save(self, *args, **kwargs):
        if not self.artist_name:
            self.artist_name = self.user.username
        if not self.email:
            self.email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.artist_name


# Saves billing address info to user profile
class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    default_street_address1 = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )
    default_street_address2 = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )
    default_town_or_city = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )
    default_county = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )
    default_postcode = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    default_country = CountryField(
        blank_label="Country",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username


# Used to save or create user changes
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile.
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
