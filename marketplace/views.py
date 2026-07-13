from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import AnnonceForm
from .models import Annonce, Echange, generer_link_code
from pokedex.models import Jeu, PokemonCache
from django.contrib import messages


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
            shiny_cherche = (
                True if form.cleaned_data['cherche_shiny'] else None
            )

            # Shiny proposé
            shiny_propose = (
                True if form.cleaned_data['propose_shiny'] else None
            )

            Annonce.objects.create(
                user=request.user,
                jeu=jeu_sv,
                pokemon_cherche_id=form.cleaned_data['pokemon_cherche_id'],
                cherche_shiny=shiny_cherche,
                cherche_nature=form.cleaned_data['cherche_nature'] or None,
                cherche_genre=form.cleaned_data['cherche_genre'] or None,
                cherche_commentaire=(
                    form.cleaned_data['cherche_commentaire'] or None
                ),
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
    annonces = Annonce.objects.filter(
        statut='ouverte'
    ).select_related('user', 'jeu')

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

    # Noms pour la recherche (proposé uniquement)
    noms_propose = {}
    for annonce in annonces:
        noms = []
        for p in annonce.propositions:
            pokemon_propose = cache.get(p['pokemon_id'])
            if pokemon_propose:
                noms.append(pokemon_propose.nom_fr.lower())
        noms_propose[annonce.pk] = ' '.join(noms)

    # Noms pour data-noms (tous)
    noms_annonces = {}
    for annonce in annonces:
        noms = []
        pokemon_cherche = cache.get(annonce.pokemon_cherche_id)
        if pokemon_cherche:
            noms.append(pokemon_cherche.nom_fr.lower())
        for p in annonce.propositions:
            pokemon_propose = cache.get(p['pokemon_id'])
            if pokemon_propose:
                noms.append(pokemon_propose.nom_fr.lower())
        noms_annonces[annonce.pk] = ' '.join(noms)

    return render(request, 'marketplace/liste_annonces.html', {
        'annonces': annonces,
        'cache': cache,
        'noms_annonces': noms_annonces,
        'noms_propose': noms_propose,
    })


@login_required
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


@login_required
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


@login_required
def detail_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    ids = set()
    ids.add(annonce.pokemon_cherche_id)
    for p in annonce.propositions:
        ids.add(p['pokemon_id'])
    cache = {
        p.pokemon_id: p
        for p in PokemonCache.objects.filter(pokemon_id__in=ids)
    }
    return render(request, 'marketplace/detail_annonce.html', {
        'annonce': annonce,
        'cache': cache,
    })


@login_required
def clore_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk, user=request.user)
    if request.method == 'POST':
        annonce.statut = 'terminee'
        annonce.save()
        return redirect('marketplace:liste_annonces')
    return render(request, 'marketplace/confirmer_cloture.html', {
        'annonce': annonce,
    })


@login_required
def proposer_echange(request, annonce_id):
    annonce = get_object_or_404(Annonce, pk=annonce_id, statut='ouverte')

    if annonce.user == request.user:
        messages.error(
            request,
            "Tu ne peux pas proposer un échange sur ta propre annonce."
        )
        return redirect('marketplace:detail_annonce', pk=annonce_id)

    echange_existant = Echange.objects.filter(
        annonce=annonce,
        user_demandeur=request.user,
        statut='en_attente'
    ).first()

    if echange_existant:
        return redirect('marketplace:detail_echange', pk=echange_existant.pk)

    # Déterminer la méthode
    if annonce.methode_echange in ('link_code', 'les_deux'):
        methode = 'link_code'
    else:
        methode = 'code_ami'

    # Créer l'échange
    link_code = generer_link_code() if methode == 'link_code' else None
    expires = (
        timezone.now() + timedelta(hours=24) if methode == 'link_code'
        else None
    )

    echange = Echange.objects.create(
        annonce=annonce,
        user_demandeur=request.user,
        methode_utilisee=methode,
        link_code=link_code,
        link_code_expires_at=expires,
        statut='en_attente'
    )

    return redirect('marketplace:detail_echange', pk=echange.pk)


@login_required
def detail_echange(request, pk):
    echange = get_object_or_404(Echange, pk=pk)

    # Seuls les deux joueurs concernés peuvent voir cette page
    if (
        request.user != echange.user_demandeur
        and request.user != echange.annonce.user
    ):
        messages.error(request, "Tu n'as pas accès à cet échange.")
        return redirect('marketplace:liste_annonces')

    return render(request, 'marketplace/detail_echange.html', {
        'echange': echange,
    })


@login_required
def confirmer_echange(request, pk):
    echange = get_object_or_404(Echange, pk=pk, statut='acceptee')

    # Vérifier que l'utilisateur est bien l'un des deux joueurs
    if (request.user != echange.user_demandeur
            and request.user != echange.annonce.user):
        messages.error(request, "Tu n'as pas accès à cet échange.")
        return redirect('marketplace:liste_annonces')

    # Enregistrer la confirmation
    if request.user == echange.user_demandeur:
        echange.confirme_demandeur = True
    else:
        echange.confirme_annonceur = True

    echange.save()

    # Si les deux ont confirmé
    if echange.confirme_demandeur and echange.confirme_annonceur:
        echange.statut = 'confirme'
        echange.confirmed_at = timezone.now()
        echange.save()

        # Incrémenter nb_echanges des deux joueurs
        echange.user_demandeur.nb_echanges += 1
        echange.user_demandeur.save()
        echange.annonce.user.nb_echanges += 1
        echange.annonce.user.save()

        # Clore l'annonce
        echange.annonce.statut = 'terminee'
        echange.annonce.save()

        messages.success(request, "🎉 Échange confirmé !")

    else:
        messages.success(
            request,
            "✅ Ta confirmation a été enregistrée. "
            "En attente de l'autre joueur."
        )

    return redirect('marketplace:detail_echange', pk=echange.pk)


@login_required
def accepter_echange(request, pk):
    echange = get_object_or_404(Echange, pk=pk, statut='en_attente')
    if request.user != echange.annonce.user:
        messages.error(request, "Tu n'as pas accès à cette action.")
        return redirect('marketplace:liste_annonces')
    if request.method == 'POST':
        echange.statut = 'acceptee'
        echange.save()
        messages.success(request, "✅ Tu as accepté cet échange.")
    return redirect('marketplace:detail_echange', pk=echange.pk)


@login_required
def refuser_echange(request, pk):
    echange = get_object_or_404(Echange, pk=pk, statut='en_attente')
    if request.user != echange.annonce.user:
        messages.error(request, "Tu n'as pas accès à cette action.")
        return redirect('marketplace:liste_annonces')
    if request.method == 'POST':
        echange.statut = 'refusee'
        echange.save()
        messages.success(request, "❌ Tu as refusé cet échange.")
    return redirect('marketplace:detail_echange', pk=echange.pk)


@login_required
def mes_echanges(request):
    echanges = Echange.objects.filter(
        user_demandeur=request.user
    ).select_related('annonce', 'annonce__user').order_by('-date_creation')

    ids = {echange.annonce.pokemon_cherche_id for echange in echanges}
    cache = {
        p.pokemon_id: p
        for p in PokemonCache.objects.filter(pokemon_id__in=ids)
    }

    return render(request, 'marketplace/mes_echanges.html', {
        'echanges': echanges,
        'cache': cache,
    })
