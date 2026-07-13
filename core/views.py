from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pokedex.models import Pokedex, PokemonCache
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

    # Cache pour les noms de Pokémon des annonces
    ids = set()
    for annonce in annonces_actives:
        ids.add(annonce.pokemon_cherche_id)
    for echange in propositions_attente:
        ids.add(echange.annonce.pokemon_cherche_id)
    cache = {
        p.pokemon_id: p
        for p in PokemonCache.objects.filter(pokemon_id__in=ids)
    }

    return render(request, 'core/tableau_de_bord.html', {
        'pokedex_progression': pokedex_progression,
        'annonces_actives': annonces_actives,
        'propositions_attente': propositions_attente,
        'cache': cache,
    })


def codes_communautaires(request):
    """Page statique des codes communautaires Écarlate & Violet."""
    cache_par_nom = {
        p.nom_fr.lower(): p
        for p in PokemonCache.objects.all()
    }

    def sprite(nom):
        pokemon = cache_par_nom.get(nom.lower())
        return pokemon.sprite_url if pokemon else None

    exclusivites_raw = [
        ('0001-0004', 'Poussacha', 'Chochodile'),
        ('0001-0007', 'Poussacha', 'Coiffeton'),
        ('0004-0007', 'Chochodile', 'Coiffeton'),
        ('0399-0400', 'Koraidon', 'Miraidon'),
        ('0166-0167', 'Carmadura', 'Malvalame'),
        ('0313-0314', 'Gouroutan', 'Quartermac'),
        ('0226-0140', 'Moufouette', 'Gloupti'),
        ('0227-0141', 'Moufflair', 'Avaltout'),
        ('0143-0114', 'Baudrive', 'Feuforêve'),
        ('0144-0115', 'Grodrive', 'Magirêve'),
        ('0276-0316', 'Draby', 'Embrylex'),
        ('0277-0317', 'Drackhaus', 'Ymphect'),
        ('0278-0318', 'Drattak', 'Tyranocif'),
        ('0305-0370', 'Fantyrm', 'Solochi'),
        ('0306-0371', 'Dispareptil', 'Diamat'),
        ('0307-0372', 'Lanssorien', 'Trioxhydre'),
        ('0319-0320', 'Dolman', 'Bekaglaçon'),
        ('0337-0339', 'Venalgue', 'Flingouste'),
        ('0338-0340', 'Kravarech', 'Gamblast'),
        ('0376-0382', 'Fort-Ivoire', 'Roue-de-Fer'),
        ('0377-0383', 'Hurle-Queue', 'Hotte-de-Fer'),
        ('0378-0384', 'Fongus-Furie', 'Paume-de-Fer'),
        ('0379-0385', 'Flotte-Mèche', 'Têtes-de-Fer'),
        ('0380-0386', 'Rampe-Ailes', 'Mite-de-Fer'),
        ('0381-0387', 'Pelage-Sablé', 'Épine-de-Fer'),
        ('0397-0398', 'Rugit-Lune', 'Garde-de-Fer'),
    ]

    evolutions_objet_raw = [
        ('0079-0079', 'Ramoloss', 'Roche Royale', 'Roigada'),
        ('0112-0112', 'Rhinoféros', 'Protecteur', 'Rhinastoc'),
        ('0117-0117', 'Hypocéan', 'Écaille Draco', 'Hyporoi'),
        ('0125-0125', 'Élektek', 'Électriseur', 'Élekable'),
        ('0126-0126', 'Magmar', 'Magmariseur', 'Maganon'),
        ('0137-0137', 'Porygon', 'Améliorateur', 'Porygon2'),
        ('0233-0233', 'Porygon2', 'CD Douteux', 'Porygon-Z'),
        ('0349-0349', 'Barpau', "Bel'Écaille", 'Milobellus'),
        ('0356-0356', 'Téraclope', 'Tissu Fauche', 'Noctunoir'),
    ]

    evolutions_sans_objet_raw = [
        ('0075-0075', 'Gravalanch', 'Grolem'),
        ('0093-0093', 'Spectrum', 'Ectoplasma'),
        ('0533-0533', 'Ouvrifier', 'Bétochef'),
        ('0708-0708', 'Brocélôme', 'Desséliande'),
    ]

    exclusivites = [
        {
            'code': c,
            'nom1': n1,
            'sprite1': sprite(n1),
            'nom2': n2,
            'sprite2': sprite(n2)
        }
        for c, n1, n2 in exclusivites_raw
    ]
    evolutions_objet = [
        {'code': c, 'nom': n, 'sprite': sprite(n), 'objet': o, 'evolution': e}
        for c, n, o, e in evolutions_objet_raw
    ]
    evolutions_sans_objet = [
        {'code': c, 'nom': n, 'sprite': sprite(n), 'evolution': e}
        for c, n, e in evolutions_sans_objet_raw
    ]

    return render(request, 'core/codes_communautaires.html', {
        'exclusivites': exclusivites,
        'evolutions_objet': evolutions_objet,
        'evolutions_sans_objet': evolutions_sans_objet,
    })
