from rest_framework import serializers
from app.models import Videojuego

class VideojuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videojuego
        fields = '__all__'