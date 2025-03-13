from django.urls import path
from app import views

app_name = 'app'
urlpatterns = [
    path('', views.ListVideogames.as_view(), name='videojuegos'),
    path('<int:game_id>/', views.lista_opiniones, name='lista_opiniones'),
    path('opiniones-recientes/', views.lista_opiniones_recientes, name='opiniones_recientes'),
    path('<int:game_id>/crear_review/', views.crear_review, name='crear_review'),
    path('mis_reviews/', views.mis_reviews, name='mis_reviews'),
    path('reviews/<int:user_id>/', views.reviews_id, name='reviews_id'),
    path('top-users/', views.top_users, name='top_users'),
    path('cambiar-avatar/', views.cambiar_avatar, name='cambiar_avatar'),
    path('registro/', views.registro, name='registro'),
]
