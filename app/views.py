from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import RegisterForm
from .models import Videojuego, Opinion, CustomUser, Comentario


# Create your views here.

class ListVideogames(LoginRequiredMixin, ListView):
    template_name = "app/lista_videojuegos.html"
    context_object_name = 'videojuegos'
    model = Videojuego

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
        context["usuario"] = self.request.user
        return context

@login_required
def lista_opiniones(request, game_id):
    videojuego = get_object_or_404(Videojuego, id=game_id)
    opiniones = Opinion.objects.filter(game_id=game_id).prefetch_related("comentarios")

    if request.method == "POST":
        texto = request.POST.get("texto")
        user_id = request.user.id
        opinion_id = request.POST.get("id_opinion")

        nuevo_comentario = Comentario(texto=texto, user_id=user_id, opinion_id=opinion_id)
        nuevo_comentario.save()

    return render(request, 'app/lista_opiniones.html', context={
        'videojuego': videojuego,
        'opiniones': opiniones,
        'usuario': request.user
    })

@login_required
def lista_opiniones_recientes(request):
    opiniones = Opinion.objects.order_by("-created_at")[:10]
    usuario = request.user

    if request.method == "POST":
        texto = request.POST.get("texto")
        user_id = request.user.id
        opinion_id = request.POST.get("id_opinion")

        nuevo_comentario = Comentario(texto=texto, user_id=user_id, opinion_id=opinion_id)
        nuevo_comentario.save()

    return render(request, 'app/lista_opiniones_recientes.html', context={"opiniones": opiniones, "usuario": usuario})

# vista basada en clase que he comentado para poder hacer el request.method.POST. Función nueva la de arriba
# class ListOpinionsRecents(LoginRequiredMixin, ListView):
#     template_name = "app/lista_opiniones_recientes.html"
#     context_object_name = 'opiniones'
#     model = Opinion
#
#     def get_queryset(self):
#         return Opinion.objects.order_by("-created_at")[:10]
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["usuario"] = self.request.user
#         return context

@login_required
def crear_review(request, game_id):
    if request.method == "POST":
        user = request.user
        game = Videojuego.objects.get(id=game_id)
        review_text = request.POST.get("review_text")
        rating = request.POST.get("rating")

        nueva_opinion = Opinion(user=user, game=game, review_text=review_text, rating=rating)
        nueva_opinion.save()

        return render(request, 'app/crear_review.html', context={"mensaje": "Opinión creada correctamente", "usuario": request.user})

    return render(request, 'app/crear_review.html', context={'usuario': request.user})


def registro(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('app:videojuegos')
    else:
        form = RegisterForm()

    return render(request, 'registration/registro.html', {'form': form})

@login_required
def mis_reviews(request):
    usuario = request.user
    opiniones = Opinion.objects.filter(user_id=usuario.id)

    return render(request, 'app/mis_reviews.html', context={'opiniones': opiniones, 'usuario': usuario})

@login_required
def reviews_id(request, user_id):
    usuario_nombre = CustomUser.objects.get(id=user_id)
    opiniones = Opinion.objects.filter(user_id=user_id)

    if request.method == "POST":
        texto = request.POST.get("texto")
        user_id = request.user.id
        opinion_id = request.POST.get("id_opinion")

        nuevo_comentario = Comentario(texto=texto, user_id=user_id, opinion_id=opinion_id)
        nuevo_comentario.save()

    return render(request, 'app/reviews_id.html', context={'opiniones': opiniones, 'usuario': request.user, 'usuario_nombre': usuario_nombre})

@login_required
def top_users(request):
    top_users = CustomUser.objects.annotate(
        num_opiniones=Count('opinions', distinct=True),
        num_comentarios=Count('comentarios', distinct=True),
    ).annotate(
        total_contribuciones=F('num_opiniones') + F('num_comentarios')
    ).order_by('-total_contribuciones')[:3]

    return render(request, 'app/top_users.html', context={'top_users': top_users, 'usuario': request.user})

@login_required
def cambiar_avatar(request):
    if request.method == "POST":
        foto = request.FILES.get("foto")
        request.user.avatar = foto
        request.user.save()

        return render(request, 'app/cambiar_avatar.html', context={'usuario': request.user, 'mensaje': "Avatar actualizado correctamente"})

    return render(request, 'app/cambiar_avatar.html', context={'usuario': request.user})

@login_required
def opinion_like(request, opinion_id):
    if request.method == "POST":
        opinion = get_object_or_404(Opinion, id=opinion_id)
        user = request.user

        if user in opinion.likes.all():
            opinion.likes.remove(user)
        else:
            opinion.likes.add(user)
            opinion.dislikes.remove(user)  # Si da like, quita dislike

        return JsonResponse({"likes": opinion.likes.count(), "dislikes": opinion.dislikes.count()})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def opinion_dislike(request, opinion_id):
    if request.method == "POST":
        opinion = get_object_or_404(Opinion, id=opinion_id)
        user = request.user

        if user in opinion.dislikes.all():
            opinion.dislikes.remove(user)
        else:
            opinion.dislikes.add(user)
            opinion.likes.remove(user)  # Si da dislike, quita like

        return JsonResponse({"likes": opinion.likes.count(), "dislikes": opinion.dislikes.count()})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def mejores_opiniones(request):
    top_opiniones = Opinion.objects.annotate(
        total_likes=Count('likes', distinct=True),
        total_dislikes=Count('dislikes', distinct=True),
    ).annotate(
        diferencia=F('total_likes') - F('total_dislikes')
    ).order_by('-diferencia')[:5]

    return render(request, 'app/top_opiniones.html', context={'top_opiniones': top_opiniones, 'usuario': request.user})

@login_required
def mis_seguidos(request):
    usuario = request.user
    mis_seguidos = usuario.follows.all()

    return render(request, "app/mis_seguidos.html", context={'usuario': usuario, 'mis_seguidos': mis_seguidos})

@login_required
def mis_seguidores(request):
    usuario = request.user
    mis_seguidores = CustomUser.objects.filter(follows=usuario)

    return render(request, "app/mis_seguidores.html", context={'usuario': usuario, 'mis_seguidores': mis_seguidores})

@login_required
def seguir_usuario(request, user_id):
    if request.method == "POST":
        usuario_a_seguir = get_object_or_404(CustomUser, id=user_id)
        usuario_actual = request.user

        if usuario_a_seguir in usuario_actual.follows.all():
            usuario_actual.follows.remove(usuario_a_seguir)
            seguido = False
        else:
            usuario_actual.follows.add(usuario_a_seguir)
            seguido = True

        return JsonResponse({"seguido": seguido})
    return JsonResponse({"error": "Método no permitido"}, status=405)


class Usuarios(LoginRequiredMixin, ListView):
    template_name = "app/usuarios.html"
    context_object_name = 'usuarios'
    model = CustomUser

    def get_queryset(self):
        queryset = CustomUser.objects.exclude(id=self.request.user.id) 
        
        busqueda = self.request.GET.get("buscar")
        if busqueda:
            queryset = queryset.filter(username__icontains=busqueda)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["usuario"] = self.request.user
        return context

@login_required
def usuario_id(request, user_id):
    usuario_id = get_object_or_404(CustomUser, id=user_id)

    return render(request, 'app/usuario_id.html', context={'user': usuario_id, 'usuario': request.user})