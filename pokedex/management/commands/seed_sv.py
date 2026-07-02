import requests
from django.core.management.base import BaseCommand
from pokedex.models import Jeu


def get_nom_francais(noms):
    for entry in noms:
        if entry['language']['name'] == 'fr':
            return entry['name']
    return None


class Command(BaseCommand):
    help = 'Seed les données Scarlet & Violet depuis PokéAPI'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Démarrage du seed Scarlet & Violet...')

        jeu, created = Jeu.objects.get_or_create(
            nom='Pokémon Écarlate & Violet',
            defaults={
                'generation': 9,
                'plateforme': 'Switch',
                'echanges_online': True,
                'pokedex_regional': [],
                'exclusivites': {
                    'ecarlate': [],
                    'violet': [],
                },
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(
                '✅ Jeu créé : Pokémon Écarlate & Violet'
            ))
        else:
            self.stdout.write('ℹ️  Jeu déjà existant, on continue...')

        self.stdout.write('🔍 Récupération du Pokédex Paldea...')

        try:
            r = requests.get(
                'https://pokeapi.co/api/v2/pokedex/paldea/',
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            self.stdout.write(self.style.SUCCESS(
                f'✅ ({len(data["pokemon_entries"])} Pokémon récupéré)'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur Pokédex : {e}'))
            return

        ids_regionaux = [
            int(entry['pokemon_species']['url'].split('/')[-2])
            for entry in data['pokemon_entries']
        ]

        jeu.pokedex_regional = ids_regionaux
        jeu.save()

        self.stdout.write(self.style.SUCCESS(
            f'✅ Seed terminé !'
            f'{len(ids_regionaux)} Pokémon dans le Pokédex Paldea.'
        ))
