from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    """
    Clase CustomUser, extiende de AbstractUser.

    avatar: Image
    follows: Relation
    rol: string

    asignar_rol: actualiza el rol del usuario
    """
    avatar = models.ImageField(default='usuario-por-defecto.png', blank=True)
    follows = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='seguidos')
    rol = models.CharField(max_length=50, blank=True, null=True, default="Crítico Novato")

    def __str__(self):
        return self.username

    def asignar_rol(self):
        """Método que actualiza el rol del usuario dependiendo del número de reviews que haya hecho."""
        total_reviews = self.opinions.count()
        if total_reviews >= 50:
            self.rol = "Leyenda del Review"
        elif total_reviews >= 30:
            self.rol = "Experto en Opiniones"
        elif total_reviews >= 15:
            self.rol = "Crítico Avanzado"
        elif total_reviews >= 5:
            self.rol = "Reseñador Aficionado"
        else:
            self.rol = "Crítico Novato"
        self.save()

class Videojuego(models.Model):
    """
    Clase Videojuego.

    title: string
    release_date: Date
    rating: float
    image: Image
    genero: string

    update_rating: actualiza el rating del videojuego
    """
    SHOOTER = 'Shooter'
    RPG = 'RPG'
    MMO = 'MMO'
    ARCADE = 'Arcade'
    HORROR = 'Horror'
    GENERO_CHOICES = [
        (SHOOTER, 'Shooter'),
        (RPG, 'Rpg'),
        (MMO, 'Mmo'),
        (ARCADE, 'Arcade'),
        (HORROR, 'Horror'),
    ]

    title = models.CharField(max_length=255, unique=True)
    release_date = models.DateField()
    rating = models.FloatField(default=0)  # Este campo se actualizará con la media
    image = models.ImageField()
    genero = models.CharField(
        max_length=20,
        choices=GENERO_CHOICES
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def update_rating(self):
        """Método para actualizar el rating del juego con la media de todas las opiniones."""
        opinions = self.opinions.all()  # Obtén todas las opiniones asociadas con este juego
        if opinions:
            average_rating = sum(opinion.rating for opinion in opinions) / opinions.count()
            self.rating = average_rating
            self.save()  # Guarda el nuevo rating en la base de datos


class Opinion(models.Model):
    """
    Clase Opinion.

    user: Relation
    game: Relation
    review_text: string
    rating: int (1 al 5)
    created_at: DateTime
    likes: Relation
    dislikes: Relation

    save: al guardar un objeto tipo Opinion, llama al update_rating y asignar_rol de los campos Videojuego y CustomUser, respectivamente.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="opinions")
    game = models.ForeignKey(Videojuego, on_delete=models.CASCADE, related_name="opinions")
    review_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Puntuación de 1 a 5
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_opinions", blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dislike_opinions", blank=True)

    # class Meta:
    #    unique_together = ("user", "game")  # Un usuario solo puede opinar una vez por juego

    def __str__(self):
        return f"Opinión de {self.user.username} sobre {self.game.title}"

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para actualizar el rating del juego cuando se guarda la opinión."""
        super().save(*args, **kwargs)  # Guarda la opinión normalmente
        self.game.update_rating()  # Actualiza el rating del juego después de guardar la opinión
        self.user.asignar_rol() # Actualiza el rol del usuario

class Comentario(models.Model):
    """
    Clase Comentario.

    user: Relation
    opinion: Relation
    texto: string
    created_at: DateTime
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios")
    opinion = models.ForeignKey(Opinion, on_delete=models.CASCADE, related_name="comentarios")
    texto = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto