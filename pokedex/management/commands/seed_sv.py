import requests
import time
from django.core.management.base import BaseCommand
from pokedex.models import Jeu


POKEDEX_REGIONAL_SV = list(range(906, 1026))  # #906 à #1025


def get_nom_francais(noms):
    for entry in noms:
        if entry['language']['name'] == 'fr':
            return entry['name']
    return None


class Command(BaseCommand):
    help = 'Seed les données Scarlet & Violet depuis PokéAPI'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Démarrage du seed Scarlet & Violet...')

        # Créer ou récupérer le jeu
        jeu, created = Jeu.objects.get_or_create(
            nom='Pokémon Écarlate & Violet',
            defaults={
                'generation': 9,
                'plateforme': 'Switch',
                'echanges_online': True,
                'pokedex_regional': POKEDEX_REGIONAL_SV,
                'exclusivites': {
                    'ecarlate': [],
                    'violet': [],
                },
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Jeu créé : Pokémon Écarlate & Violet'))
        else:
            self.stdout.write('ℹ️  Jeu déjà existant, on continue...')

        # Récupérer les exclusivités depuis PokéAPI
        self.stdout.write('🔍 Récupération des exclusivités de version...')
        ecarlate = []
        violet = []

        try:
            r = requests.get('https://pokeapi.co/api/v2/version-group/scarlet-violet/')
            r.raise_for_status()
            data = r.json()
            self.stdout.write(self.style.SUCCESS('✅ Connexion PokéAPI OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur PokéAPI : {e}'))
            return

        # Récupérer les exclusivités Écarlate
        try:
            r = requests.get('https://pokeapi.co/api/v2/version/scarlet/')
            data = r.json()
            for entry in data.get('version_group', {}).get('pokemon_entries', []):
                pass  # structure différente, on passe par le Pokédex
        except Exception:
            pass

        # Récupérer via le Pokédex de version
        for version_id, liste in [('paldea', POKEDEX_REGIONAL_SV)]:
            try:
                r = requests.get(f'https://pokeapi.co/api/v2/pokedex/paldea/')
                r.raise_for_status()
                data = r.json()
                self.stdout.write(self.style.SUCCESS(f'✅ Pokédex Paldea récupéré ({len(data["pokemon_entries"])} Pokémon)'))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Erreur Pokédex : {e}'))
                return

        # Mettre à jour le jeu avec le vrai Pokédex régional
        ids_regionaux = [entry['pokemon_species']['url'].split('/')[-2]
                         for entry in data['pokemon_entries']]
        ids_regionaux = [int(i) for i in ids_regionaux]

        jeu.pokedex_regional = ids_regionaux
        jeu.save()

        self.stdout.write(self.style.SUCCESS(
            f'✅ Seed terminé ! {len(ids_regionaux)} Pokémon dans le Pokédex Paldea.'
        ))
