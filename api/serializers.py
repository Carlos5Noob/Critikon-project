from rest_framework import serializers
from app.models import Videojuego

class VideojuegoSerializer(serializers.ModelSerializer):
    """
    Serializador de la clase Videojuego.
    """
    class Meta:
        model = Videojuego
        fields = '__all__'