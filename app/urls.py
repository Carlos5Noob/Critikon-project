from django.urls import path
from app import views


urlpatterns = [
    path('', views.ListVideogames.as_view(), name='videojuegos'),
]
