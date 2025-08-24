from django.urls import path
from . import views

urlpatterns = [
    path('', views.bag, name="bag"),
    path('add/<id>/', views.add_to_bag, name='add_to_bag'),
    path('edit_bag/<int:artist_id>/', views.edit_bag, name='edit_bag'),
    path(
        'remove_commission/<str:bag_id>/',
        views.remove_commission,
        name='remove_commission',
    ),
]
