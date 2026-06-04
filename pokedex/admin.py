from django.contrib import admin
from .models import Jeu, Pokedex, PokemonCache

admin.site.register(Jeu)
admin.site.register(Pokedex)
admin.site.register(PokemonCache)
