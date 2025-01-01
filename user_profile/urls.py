from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('create/', views.create, name='create'),
    path('api/tags/', views.get_tags, name='get_tags'),
]
