import requests
import time
from django.core.management.base import BaseCommand
from pokedex.models import Jeu, PokemonCache


def get_nom_francais(noms):
    for entry in noms:
        if entry['language']['name'] == 'fr':
            return entry['name']
    return None


def get_types_francais(types):
    TYPES_FR = {
        'normal': 'normal', 'fire': 'feu', 'water': 'eau',
        'electric': 'électrik', 'grass': 'plante', 'ice': 'glace',
        'fighting': 'combat', 'poison': 'poison', 'ground': 'sol',
        'flying': 'vol', 'psychic': 'psy', 'bug': 'insecte',
        'rock': 'roche', 'ghost': 'spectre', 'dragon': 'dragon',
        'dark': 'ténèbres', 'steel': 'acier', 'fairy': 'fée',
    }
    return [TYPES_FR.get(t['type']['name'], t['type']['name']) for t in types]


def get_nom_talent_francais(ability_name):
    try:
        r = requests.get(
            f'https://pokeapi.co/api/v2/ability/{ability_name}/',
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        for entry in data['names']:
            if entry['language']['name'] == 'fr':
                return entry['name']
        return ability_name
    except Exception:
        return ability_name


def get_talents(abilities):
    resultats = []
    for entry in abilities:
        nom_fr = get_nom_talent_francais(entry['ability']['name'])
        resultats.append({
            'nom': nom_fr,
            'cache': entry['is_hidden'],
        })
    return resultats


class Command(BaseCommand):
    help = (
        'Remplit le cache PokéAPI '
        '(noms FR, sprites, types, talents) pour S/V'
    )

    def handle(self, *args, **kwargs):
        try:
            jeu = Jeu.objects.get(nom='Pokémon Écarlate & Violet')
        except Jeu.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                '❌ Jeu S/V introuvable. Lance seed_sv d\'abord.'
            ))
            return

        ids = jeu.pokedex_regional
        total = len(ids)
        self.stdout.write(f'🔍 Cache de {total} Pokémon à remplir...')

        ok = 0
        erreurs = 0

        for i, pokemon_id in enumerate(ids, 1):
            try:
                # Récupérer nom FR
                r_species = requests.get(
                    f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/',
                    timeout=10
                )
                r_species.raise_for_status()
                species_data = r_species.json()
                nom_fr = get_nom_francais(species_data['names'])
                if not nom_fr:
                    nom_fr = species_data['name']

                # Récupérer sprite + types + talents
                r_pokemon = requests.get(
                    f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/',
                    timeout=10
                )
                r_pokemon.raise_for_status()
                pokemon_data = r_pokemon.json()

                sprite_url = pokemon_data['sprites']['front_default'] or ''
                types = get_types_francais(pokemon_data['types'])
                talents = get_talents(pokemon_data['abilities'])

                PokemonCache.objects.update_or_create(
                    pokemon_id=pokemon_id,
                    defaults={
                        'nom_fr': nom_fr,
                        'sprite_url': sprite_url,
                        'types': types,
                        'talents': talents,
                    }
                )

                ok += 1
                self.stdout.write(f'  [{i}/{total}] #{pokemon_id} {nom_fr} ✅')
                time.sleep(0.3)

            except Exception as e:
                erreurs += 1
                self.stdout.write(self.style.ERROR(
                    f'  [{i}/{total}] #{pokemon_id} ❌ {e}'
                ))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Cache terminé ! {ok} OK, '
            f'{erreurs} erreurs.'
        ))
