from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
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
    return render(request, 'accounts/inscription.html', {'form': form})


def envoyer_email_confirmation(request, user):
    """Génère et envoie le lien d'activation par email."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    lien = f"http://{request.get_host()}/auth/activer/{uid}/{token}/"
    send_mail(
        subject="Active ton compte PokéMarket 🎮",
        message=f"Salut {user.pseudo} !\n\nClique sur ce lien pour activer ton compte :\n{lien}\n\nÀ tout de suite sur PokéMarket !",
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
    return render(request, 'accounts/connexion.html', {'form': form})


def deconnexion(request):
    """Déconnexion."""
    logout(request)
    return redirect('/')
