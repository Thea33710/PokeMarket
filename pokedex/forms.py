from django import forms
from .models import Pokedex, Jeu


class PokedexForm(forms.ModelForm):
    class Meta:
        model = Pokedex
        fields = ['nom', 'jeu', 'type_vue', 'mode_shiny']
        labels = {
            'nom': 'Nom du Pokédex',
            'jeu': 'Jeu',
            'type_vue': 'Type de vue',
            'mode_shiny': 'Activer le suivi Shiny',
        }
        widgets = {
            'nom': forms.TextInput(
                attrs={'placeholder': 'Ex : Ma partie Écarlate'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jeu'].queryset = Jeu.objects.filter(echanges_online=True)
