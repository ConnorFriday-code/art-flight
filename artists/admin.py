from django.contrib import admin
from .models import Artist, Tag

# Register your models here.

admin.site.register(Artist)
admin.site.register(Tag)