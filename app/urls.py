from django.urls import path
from app import views

app_name = 'app'
urlpatterns = [
    path('', views.ListVideogames.as_view(), name='videojuegos'),
    path('<int:game_id>/', views.lista_opiniones, name='lista_opiniones'),
]
