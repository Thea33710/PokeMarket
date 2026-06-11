from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import AnnonceForm
from .models import Annonce
from pokedex.models import Jeu, PokemonCache


@login_required
def creer_annonce(request):
    jeu_sv = Jeu.objects.get(nom__icontains='Écarlate')

    if request.method == 'POST':
        form = AnnonceForm(request.POST)
        if form.is_valid():
            duree = int(form.cleaned_data['duree'])

            # Construire les IVs cherchés
            ivs_cherche = {}
            for stat in ['pv', 'atk', 'def', 'spa', 'spd', 'spe']:
                val = form.cleaned_data.get(f'iv_{stat}')
                if val is not None:
                    ivs_cherche[stat] = val
            ivs_cherche = ivs_cherche or None

            # Talents cochés
            talents_cherche = request.POST.getlist('cherche_talents') or None
            talents_propose = request.POST.getlist('propose_talents') or None

            # Construire les IVs proposés
            ivs_propose = {}
            for stat in ['pv', 'atk', 'def', 'spa', 'spd', 'spe']:
                val = form.cleaned_data.get(f'propose_iv_{stat}')
                if val is not None:
                    ivs_propose[stat] = val
            ivs_propose = ivs_propose or None

            # Shiny cherché
            shiny_cherche = True if form.cleaned_data['cherche_shiny'] else None

            # Shiny proposé
            shiny_propose = True if form.cleaned_data['propose_shiny'] else None

            Annonce.objects.create(
                user=request.user,
                jeu=jeu_sv,
                pokemon_cherche_id=form.cleaned_data['pokemon_cherche_id'],
                cherche_shiny=shiny_cherche,
                cherche_nature=form.cleaned_data['cherche_nature'] or None,
                cherche_genre=form.cleaned_data['cherche_genre'] or None,
                cherche_commentaire=form.cleaned_data['cherche_commentaire'] or None,
                cherche_ivs_min=ivs_cherche,
                cherche_talents=talents_cherche,
                propositions=[{
                    'pokemon_id': form.cleaned_data['pokemon_propose_id'],
                    'shiny': shiny_propose,
                    'nature': form.cleaned_data['propose_nature'] or None,
                    'talents': talents_propose,
                    'genre': form.cleaned_data['propose_genre'] or None,
                    'ivs': ivs_propose,
                }],
                methode_echange=form.cleaned_data['methode_echange'],
                expires_at=timezone.now() + timedelta(days=duree),
            )
            return redirect('marketplace:liste_annonces')
    else:
        form = AnnonceForm()

    return render(request, 'marketplace/creer_annonce.html', {'form': form})


@login_required
def liste_annonces(request):
    annonces = Annonce.objects.filter(statut='ouverte').select_related('user', 'jeu')

    # Récupérer tous les IDs Pokémon présents dans les annonces
    ids = set()
    for annonce in annonces:
        ids.add(annonce.pokemon_cherche_id)
        for p in annonce.propositions:
            ids.add(p['pokemon_id'])

    # Charger le cache une seule fois
    cache = {
        p.pokemon_id: p
        for p in PokemonCache.objects.filter(pokemon_id__in=ids)
    }

    return render(request, 'marketplace/liste_annonces.html', {
        'annonces': annonces,
        'cache': cache,
    })


def autocomplete_pokemon(request):
    query = request.GET.get('q', '').strip()
    resultats = []
    if len(query) >= 2:
        resultats = PokemonCache.objects.filter(
            nom_fr__icontains=query
        ).order_by('pokemon_id')[:10]
    return render(request, 'marketplace/autocomplete.html', {
        'resultats': resultats
    })


def talents_pokemon(request):
    pokemon_id = request.GET.get('pokemon_id')
    cible = request.GET.get('cible', 'cherche')
    talents = []
    if pokemon_id:
        try:
            pokemon = PokemonCache.objects.get(pokemon_id=pokemon_id)
            talents = pokemon.talents
        except PokemonCache.DoesNotExist:
            pass
    return render(request, 'marketplace/talents.html', {
        'talents': talents,
        'cible': cible,
    })
