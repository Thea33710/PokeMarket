import requests
import time
from django.core.management.base import BaseCommand
from pokedex.models import PokemonCache
from .cache_pokeapi import get_nom_francais, get_types_francais, get_talents


class Command(BaseCommand):
    help = 'Cache des Pokémon spécifiques par ID national (hors Pokédex S/V)'

    def add_arguments(self, parser):
        parser.add_argument('ids', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        ids = kwargs['ids']
        for pokemon_id in ids:
            try:
                r_species = requests.get(
                    f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/',
                    timeout=10
                )
                r_species.raise_for_status()
                nom_fr = get_nom_francais(r_species.json()['names'])

                r_pokemon = requests.get(
                    f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/',
                    timeout=10
                )
                r_pokemon.raise_for_status()
                pokemon_data = r_pokemon.json()

                PokemonCache.objects.update_or_create(
                    pokemon_id=pokemon_id,
                    defaults={
                        'nom_fr': nom_fr or pokemon_data['name'],
                        'sprite_url': pokemon_data['sprites']['front_default'] or '',
                        'types': get_types_francais(pokemon_data['types']),
                        'talents': get_talents(pokemon_data['abilities']),
                    }
                )
                self.stdout.write(f'#{pokemon_id} {nom_fr} ✅')
                time.sleep(0.3)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'#{pokemon_id} ❌ {e}'))
