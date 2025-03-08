from django.db import models
from django.contrib.auth.models import User

class Videojuego(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opinions")
    game = models.ForeignKey(Videojuego, on_delete=models.CASCADE, related_name="opinions")
    review_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Puntuación de 1 a 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "game")  # Un usuario solo puede opinar una vez por juego

    def __str__(self):
        return f"Opinión de {self.user.username} sobre {self.game.title}"

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para actualizar el rating del juego cuando se guarda la opinión."""
        super().save(*args, **kwargs)  # Guarda la opinión normalmente
        self.game.update_rating()  # Actualiza el rating del juego después de guardar la opinión
