from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from pokedex.models import PokemonCache
from marketplace.models import Echange
from .forms import InscriptionForm
from .models import User


def inscription(request):
    """Page d'inscription."""
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Envoyer l'email de confirmation
            envoyer_email_confirmation(request, user)
            messages.success(request, "Compte créé ! Vérifie tes emails pour activer ton compte 📧")
            return redirect('auth:connexion')
    else:
        form = InscriptionForm()
    return render(request, 'auth/inscription.html', {'form': form})


def envoyer_email_confirmation(request, user):
    """Génère et envoie le lien d'activation par email."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    lien = f"http://{request.get_host()}/auth/activer/{uid}/{token}/"
    message = (
        f"Salut {user.pseudo} !\n\n"
        f"Clique sur ce lien pour activer ton compte :\n{lien}\n\n"
        f"À tout de suite sur PokéMarket !"
    )
    send_mail(
        subject="Active ton compte PokéMarket 🎮",
        message=message,
        from_email="noreply@pokemarket.com",
        recipient_list=[user.email],
    )


def activer_compte(request, uidb64, token):
    """Active le compte après clic sur le lien email."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Compte activé ! Tu peux te connecter 🎉")
        return redirect('auth:connexion')
    else:
        messages.error(request, "Ce lien est invalide ou expiré 😕")
        return redirect('auth:inscription')


def connexion(request):
    """Page de connexion."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Email ou mot de passe incorrect 😕")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/connexion.html', {'form': form})


def deconnexion(request):
    """Déconnexion."""
    logout(request)
    return redirect('/')


@login_required
def profil(request):
    """Page profil utilisateur."""
    # Échanges en cours où l'utilisateur est demandeur
    echanges_demandes = Echange.objects.filter(
        user_demandeur=request.user,
        statut='en_attente'
    ).select_related('annonce', 'annonce__user')

    # Échanges en cours sur les annonces de l'utilisateur
    echanges_recus = Echange.objects.filter(
        annonce__user=request.user,
        statut='en_attente'
    ).select_related('annonce', 'user_demandeur')

    return render(request, 'accounts/profil.html', {
        'echanges_demandes': echanges_demandes,
        'echanges_recus': echanges_recus,
    })


@login_required
def changer_avatar(request):
    """Page de changement d'avatar."""
    couleurs = [
        '#7030a0', '#4a1472', '#e91e63', '#f44336',
        '#ff9800', '#4caf50', '#2196f3', '#009688',
    ]

    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_avatar_id')
        couleur = request.POST.get('avatar_couleur')

        if pokemon_id and PokemonCache.objects.filter(
            pokemon_id=pokemon_id
        ).exists():
            request.user.pokemon_avatar_id = pokemon_id
        if couleur in couleurs:
            request.user.avatar_couleur = couleur
        request.user.save()

        messages.success(request, "Avatar mis à jour ! 🎉")
        return redirect('auth:profil')

    return render(request, 'accounts/changer_avatar.html', {
        'couleurs': couleurs,
    })
