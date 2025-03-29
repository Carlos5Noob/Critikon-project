from django.urls import path
from app import views

app_name = 'app'
urlpatterns = [
    path('', views.ListVideogames.as_view(), name='videojuegos'),
    path('<int:game_id>/', views.lista_opiniones, name='lista_opiniones'),
    path('opiniones-recientes/', views.lista_opiniones_recientes, name='opiniones_recientes'),
    path('<int:game_id>/crear_review/', views.crear_review, name='crear_review'),
    path('mis-reviews/', views.mis_reviews, name='mis_reviews'),
    path('reviews/<int:user_id>/', views.reviews_id, name='reviews_id'),
    path('top-users/', views.top_users, name='top_users'),
    path('cambiar-avatar/', views.cambiar_avatar, name='cambiar_avatar'),
    path('opinion/<int:opinion_id>/like/', views.opinion_like, name='opinion_like'),
    path('opinion/<int:opinion_id>/dislike/', views.opinion_dislike, name='opinion_dislike'),
    path('top-opinions/', views.mejores_opiniones, name='mejores_opiniones'),
    path('mis-seguidos/', views.mis_seguidos, name='mis_seguidos'),
    path('mis-seguidores/', views.mis_seguidores, name='mis_seguidores'),
    path('seguir-usuario/<int:user_id>/', views.seguir_usuario, name='seguir_usuario'),
    path('registro/', views.registro, name='registro'),
]
