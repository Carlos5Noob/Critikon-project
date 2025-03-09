from django.contrib import admin
from app.models import Videojuego, Opinion, CustomUser

# Register your models here.

admin.site.register(Videojuego)
admin.site.register(Opinion)
admin.site.register(CustomUser)