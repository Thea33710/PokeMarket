from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Annonce
from pokedex.models import PokemonCache

NATURES = [
    ('', 'Indifférent'),
    ('rigide', 'Rigide'), ('solitaire', 'Solitaire'),
    ('brave', 'Brave'), ('malicieux', 'Malicieux'),
    ('hardi', 'Hardi'), ('docile', 'Docile'),
    ('relaxe', 'Relaxé'), ('balourd', 'Balourd'),
    ('timide', 'Timide'), ('hatif', 'Hâtif'),
    ('serieux', 'Sérieux'), ('jovial', 'Jovial'),
    ('naif', 'Naïf'), ('modeste', 'Modeste'),
    ('doux', 'Doux'), ('calme', 'Calme'),
    ('gentil', 'Gentil'), ('pudique', 'Pudique'),
    ('lache', 'Lâche'), ('pressé', 'Pressé'),
    ('mauvais', 'Mauvais'), ('bizarre', 'Bizarre'),
    ('malpoli', 'Malpoli'), ('furieux', 'Furieux'),
    ('prudent', 'Prudent'),
]

TALENTS = [
    ('', 'Indifférent'),
    ('normal', 'Normal'),
    ('cache', 'Talent caché'),
]

GENRES = [
    ('', 'Indifférent'),
    ('male', 'Mâle'),
    ('femelle', 'Femelle'),
]

DUREES = [
    (7, '7 jours'),
    (14, '14 jours'),
    (30, '30 jours'),
]


class AnnonceForm(forms.Form):

    # Pokémon recherché
    pokemon_cherche_id = forms.IntegerField(
        label='Pokémon recherché (numéro Pokédex)',
        min_value=1,
    )

    # Précisions optionnelles
    cherche_shiny = forms.NullBooleanField(
        label='Shiny ?',
        required=False,
        widget=forms.Select(choices=[
            (None, 'Indifférent'),
            (True, 'Oui'),
            (False, 'Non'),
        ])
    )
    cherche_nature = forms.ChoiceField(
        label='Nature',
        choices=NATURES,
        required=False,
    )
    cherche_talent = forms.ChoiceField(
        label='Talent',
        choices=TALENTS,
        required=False,
    )
    cherche_genre = forms.ChoiceField(
        label='Genre',
        choices=GENRES,
        required=False,
    )
    cherche_commentaire = forms.CharField(
        label='Commentaire libre',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )

    # Pokémon proposé (1 seul pour le MVP)
    pokemon_propose_id = forms.IntegerField(
        label='Pokémon proposé (numéro Pokédex)',
        min_value=1,
    )

    # Méthode d'échange
    methode_echange = forms.ChoiceField(
        label="Méthode d'échange",
        choices=Annonce.METHODE_CHOICES,
    )

    # Durée
    duree = forms.ChoiceField(
        label='Durée de l\'annonce',
        choices=DUREES,
    )
