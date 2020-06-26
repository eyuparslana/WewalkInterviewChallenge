from django.urls import path

from api import views

urlpatterns = [
    path('places/', views.get_places_on_route, name='search'),
    path('favourites/', views.favourites, name='favourites')
]