from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pokedex.models import Pokedex
from marketplace.models import Annonce, Echange


def accueil(request):
    """
    Page d'accueil publique.
    Redirige vers le tableau de bord si connecté.
    """
    if request.user.is_authenticated:
        return redirect('core:tableau_de_bord')
    return render(request, 'core/accueil.html')


@login_required
def tableau_de_bord(request):
    """Tableau de bord après connexion."""
    pokedex_list = Pokedex.objects.filter(
        user=request.user
    ).select_related('jeu')

    pokedex_progression = []
    for pokedex in pokedex_list:
        total = len(pokedex.jeu.pokedex_regional)
        captures = sum(
            1 for s in pokedex.pokemon_statuses.values()
            if s == 'capture'
        )
        pokedex_progression.append({
            'pokedex': pokedex,
            'captures': captures,
            'total': total,
        })

    annonces_actives = Annonce.objects.filter(
        user=request.user,
        statut='ouverte'
    )

    propositions_attente = Echange.objects.filter(
        annonce__user=request.user,
        statut='en_attente'
    ).select_related('annonce', 'user_demandeur')

    return render(request, 'core/tableau_de_bord.html', {
        'pokedex_progression': pokedex_progression,
        'annonces_actives': annonces_actives,
        'propositions_attente': propositions_attente,
    })


def codes_communautaires(request):
    """Page statique des codes communautaires Écarlate & Violet."""
    return render(request, 'core/codes_communautaires.html')
