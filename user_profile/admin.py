from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Artist

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sku', 'tag', 'description')
    search_fields = ('sku', 'user__username', 'tag')
    ordering = ('id',)