from django.contrib import admin
from app.models import Videojuego, Opinion, CustomUser, Comentario

# Register your models here.

admin.site.register(Videojuego)
admin.site.register(Opinion)
admin.site.register(CustomUser)
admin.site.register(Comentario)