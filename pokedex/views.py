from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pokedex, PokemonCache
from .forms import PokedexForm


@login_required
def liste_pokedex(request):
    pokedex_list = Pokedex.objects.filter(user=request.user).select_related('jeu')
    return render(request, 'pokedex/liste_pokedex.html', {'pokedex_list': pokedex_list})


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
                'statut': pokedex.pokemon_statuses.get(str(pokemon_id), 'non_vu'),
            })

    captures = sum(1 for e in entrees if e['statut'] == 'capture')
    total = len(entrees)

    return render(request, 'pokedex/detail_pokedex.html', {
        'pokedex': pokedex,
        'entrees': entrees,
        'captures': captures,
        'total': total,
    })
