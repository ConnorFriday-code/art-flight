from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.bag, name="bag"),
    path('add/<id>/', views.add_to_bag, name='add_to_bag'),
]
