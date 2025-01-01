from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_artists, name="artists"),
    path('<sku>', views.artists_details, name="artists_details"),
]