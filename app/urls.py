from django.urls import path
from app import views

app_name = 'app'
urlpatterns = [
    path('', views.ListVideogames.as_view(), name='videojuegos'),
    path('<int:game_id>/', views.lista_opiniones, name='lista_opiniones'),
    path('opiniones-recientes/', views.ListOpinionsRecents.as_view(), name='opiniones_recientes'),
    path('<int:game_id>/crear_review/', views.crear_review, name='crear_review'),
]
