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

        # Búsqueda
        busqueda = self.request.GET.get("buscar")
        if busqueda:
            queryset = queryset.filter(title__icontains=busqueda)

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

class ListOpinionsRecents(ListView):
    template_name = "app/lista_opiniones_recientes.html"
    context_object_name = 'opiniones'

    def get_queryset(self):
        return Opinion.objects.order_by("-created_at")[:10]


def crear_review(request, game_id):
    if request.method == "POST":
        user = request.user
        game = Videojuego.objects.get(id=game_id)
        review_text = request.POST.get("review_text")
        rating = request.POST.get("rating")

        nueva_opinion = Opinion(user=user, game=game, review_text=review_text, rating=rating)
        nueva_opinion.save()

        return render(request, 'app/crear_review.html', context={"mensaje": "Opinión creada correctamente"})

    return render(request, 'app/crear_review.html')