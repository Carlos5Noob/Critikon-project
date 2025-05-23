from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from app.models import Videojuego
from .serializers import VideojuegoSerializer

class VideojuegoViewSet(viewsets.ModelViewSet):
    """
    View que recoge los objetos de la clase Videojuego.
    """
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ApiRootViewSet(viewsets.ViewSet):
    """
    View que recoge la API Root
    """
    def list(self, request):
        return Response({
            'videojuegos': request.build_absolute_uri(reverse('api:videojuego-list', request=request)),
        })