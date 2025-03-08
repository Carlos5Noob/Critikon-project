from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Videojuego, Opinion

# Create your views here.

class ListVideogames(ListView):
    template_name = "app/lista_videojuegos.html"
    context_object_name = 'videojuegos'

    def get_queryset(self):
        queryset = Videojuego.objects.all()

        # Filtro por género
        genero = self.request.GET.get("genero")
        if genero:
            queryset = queryset.filter(genero=genero)

        # Ordenación
        orden = self.request.GET.get("orden")
        if orden:
            if orden == "title":
                queryset = queryset.order_by("title")
            elif orden == "-title":
                queryset = queryset.order_by("-title")
            elif orden == "release_date":
                queryset = queryset.order_by("release_date")
            elif orden == "-release_date":
                queryset = queryset.order_by("-release_date")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["generos"] = Videojuego.GENERO_CHOICES
        return context


def lista_opiniones(request, game_id):
    videojuego = get_object_or_404(Videojuego, id=game_id)
    opiniones = Opinion.objects.filter(game_id=game_id)

    return render(request, 'app/lista_opiniones.html', context={
        'videojuego': videojuego,
        'opiniones': opiniones
    })