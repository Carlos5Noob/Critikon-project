from django.urls import path, include
from rest_framework import routers
from .views import VideojuegoViewSet, ApiRootViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'videojuegos', VideojuegoViewSet)
router.register(r'', ApiRootViewSet, basename='api-root')

urlpatterns = [
    path('', include(router.urls)),
]