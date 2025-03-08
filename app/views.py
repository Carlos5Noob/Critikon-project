from django.shortcuts import render
from django.views.generic import ListView
from .models import Videojuego

# Create your views here.

class ListVideogames(ListView):
    template_name = "app/lista_videojuegos.html"
    context_object_name = 'videojuegos'

    def get_queryset(self):
        return  Videojuego.objects.all()

