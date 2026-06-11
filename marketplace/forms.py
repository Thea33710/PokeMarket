from django import forms
from .models import Annonce

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
    ('lache', 'Lâche'), ('presse', 'Pressé'),
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

    # Pokémon recherché (champ caché — rempli par l'autocomplete)
    pokemon_cherche_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    # Obligatoires
    cherche_shiny = forms.BooleanField(
        label='✨ Shiny uniquement',
        required=False,
    )
    

    # Optionnels
    cherche_nature = forms.ChoiceField(
        label='Nature',
        choices=NATURES,
        required=False,
    )
    cherche_genre = forms.MultipleChoiceField(
        label='Genre souhaité',
        choices=[('male', 'Mâle'), ('femelle', 'Femelle')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    cherche_commentaire = forms.CharField(
        label='Commentaire libre',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )

    # IVs optionnels (0-31 par stat)
    iv_pv = forms.IntegerField(
        label='IVs PV minimum',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    iv_atk = forms.IntegerField(
        label='IVs Attaque minimum',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    iv_def = forms.IntegerField(
        label='IVs Défense minimum',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    iv_spa = forms.IntegerField(
        label='IVs Att. Spé minimum',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    iv_spd = forms.IntegerField(
        label='IVs Déf. Spé minimum',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    iv_spe = forms.IntegerField(
        label='IVs Vitesse minimum',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )

    # Pokémon proposé (champ caché — rempli par l'autocomplete)
    pokemon_propose_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    # Mêmes champs pour le proposé
    propose_shiny = forms.BooleanField(
        label='✨ Mon Pokémon est shiny',
        required=False,
    )
    propose_genre = forms.MultipleChoiceField(
        label='Genre du Pokémon proposé',
        choices=[('male', 'Mâle'), ('femelle', 'Femelle')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    propose_nature = forms.ChoiceField(
        label='Nature',
        choices=NATURES,
        required=False,
    )
    propose_talent = forms.ChoiceField(
        label='Talent',
        choices=TALENTS,
        required=False,
    )
    propose_iv_pv = forms.IntegerField(
        label='IVs PV',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    propose_iv_atk = forms.IntegerField(
        label='IVs Attaque',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    propose_iv_def = forms.IntegerField(
        label='IVs Défense',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    propose_iv_spa = forms.IntegerField(
        label='IVs Att. Spé',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    propose_iv_spd = forms.IntegerField(
        label='IVs Déf. Spé',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )
    propose_iv_spe = forms.IntegerField(
        label='IVs Vitesse',
        required=False, min_value=0, max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '0-31'}),
    )

    # Paramètres
    methode_echange = forms.ChoiceField(
        label="Méthode d'échange",
        choices=Annonce.METHODE_CHOICES,
    )
    duree = forms.ChoiceField(
        label="Durée de l'annonce",
        choices=DUREES,
    )
