from datetime import date
from django.db import migrations

def poblar_videojuegos(apps, schema_editor):
    Videojuego = apps.get_model('app', 'Videojuego')
    Videojuego.objects.create(title='Pokemon Diamante Brillante', release_date=date(2021, 11, 19), rating=0, image='pkm-diamante.jpg', genero='RPG')
    Videojuego.objects.create(title='The Last Of Us Part II', release_date=date(2020, 6, 19), rating=0, image='tlou.jpg', genero='Arcade')
    Videojuego.objects.create(title='Grand Theft Auto VI', release_date=date(2025, 5, 18), rating=0, image='gta6.jpg', genero='RPG')

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(poblar_videojuegos),
    ]