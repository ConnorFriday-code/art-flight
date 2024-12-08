from django.contrib import admin
from .models import Artist, Tag

# Register your models here.

class ArtistAdmin(admin.ModelAdmin):
    list_display=(
        'artist_name',
        'sku',
        'tag',
        'description',
        'price',
        'image',
        'dos',
        'donts',
    )
    ordering=('sku',)

class TagAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Tag, TagAdmin)