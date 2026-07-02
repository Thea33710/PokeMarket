from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Pokedex, PokemonCache
from .forms import PokedexForm


@login_required
def liste_pokedex(request):
    pokedex_list = Pokedex.objects.filter(
        user=request.user
    ).select_related('jeu')
    return render(
        request,
        'pokedex/liste_pokedex.html',
        {'pokedex_list': pokedex_list}
    )


@login_required
def creer_pokedex(request):
    if request.method == 'POST':
        form = PokedexForm(request.POST)
        if form.is_valid():
            pokedex = form.save(commit=False)
            pokedex.user = request.user
            pokedex.pokemon_statuses = {}
            pokedex.save()
            return redirect('pokedex:detail', pk=pokedex.pk)
    else:
        form = PokedexForm()
    return render(request, 'pokedex/creer_pokedex.html', {'form': form})


@login_required
def detail_pokedex(request, pk):
    pokedex = get_object_or_404(Pokedex, pk=pk, user=request.user)
    jeu = pokedex.jeu

    ids = jeu.pokedex_regional
    pokemon_list = PokemonCache.objects.filter(pokemon_id__in=ids)
    pokemon_dict = {p.pokemon_id: p for p in pokemon_list}

    entrees = []
    for pokemon_id in ids:
        cache = pokemon_dict.get(pokemon_id)
        if cache:
            entrees.append({
                'id': pokemon_id,
                'nom': cache.nom_fr,
                'sprite': cache.sprite_url,
                'types': cache.types,
                'statut': pokedex.pokemon_statuses.get(
                    str(pokemon_id),
                    'non_vu'
                ),
            })

    captures = sum(1 for e in entrees if e['statut'] == 'capture')
    shinies = 0
    if pokedex.mode_shiny and pokedex.shiny_statuses:
        shinies = sum(
            1 for pid in pokedex.shiny_statuses
            if pokedex.shiny_statuses[str(pid)]
        )
    total = len(entrees)

    # Types disponibles pour le filtre
    types_set = set()
    for entree in entrees:
        for t in entree['types']:
            types_set.add(t)
    types_disponibles = sorted(types_set)

    return render(request, 'pokedex/detail_pokedex.html', {
        'pokedex': pokedex,
        'entrees': entrees,
        'captures': captures,
        'total': total,
        'shinies': shinies,
        'types_disponibles': types_disponibles,
    })


@login_required
@require_POST
def marquer_pokemon(request, pk, pokemon_id, action):
    pokedex = get_object_or_404(Pokedex, pk=pk, user=request.user)

    statut_actuel = pokedex.pokemon_statuses.get(str(pokemon_id), 'non_vu')
    nouveau_statut = statut_actuel  # par défaut on ne change pas

    if action == 'vu':
        if statut_actuel in ('non_vu', 'capture'):
            nouveau_statut = 'vu'
        else:
            nouveau_statut = 'non_vu'

    elif action == 'capture':
        if statut_actuel == 'capture':
            nouveau_statut = 'vu'
        else:
            nouveau_statut = 'capture'

    elif action == 'shiny' and pokedex.mode_shiny:
        if pokedex.shiny_statuses is None:
            pokedex.shiny_statuses = {}
        shiny_actuel = pokedex.shiny_statuses.get(str(pokemon_id), False)
        pokedex.shiny_statuses[str(pokemon_id)] = not shiny_actuel

    pokedex.pokemon_statuses[str(pokemon_id)] = nouveau_statut
    pokedex.save()

    cache = PokemonCache.objects.get(pokemon_id=pokemon_id)
    shiny = (pokedex.mode_shiny and pokedex.shiny_statuses
             and pokedex.shiny_statuses.get(str(pokemon_id), False))

    # Recalculer progression
    captures = sum(
        1 for s in pokedex.pokemon_statuses.values()
        if s == 'capture'
    )
    total = len(pokedex.jeu.pokedex_regional)
    shinies = 0
    if pokedex.mode_shiny and pokedex.shiny_statuses:
        shinies = sum(1 for v in pokedex.shiny_statuses.values() if v)

    return render(request, 'pokedex/fragments/marquer_response.html', {
        'entree': {
            'id': pokemon_id,
            'nom': cache.nom_fr,
            'sprite': cache.sprite_url,
            'types': cache.types,
            'statut': nouveau_statut,
            'shiny': shiny,
        },
        'pokedex': pokedex,
        'captures': captures,
        'total': total,
        'shinies': shinies,
    })


@login_required
def supprimer_pokedex(request, pk):
    pokedex = get_object_or_404(Pokedex, pk=pk, user=request.user)
    if request.method == 'POST':
        pokedex.delete()
        return redirect('pokedex:liste')
    return render(request, 'pokedex/confirmer_suppression.html', {
        'pokedex': pokedex,
    })
