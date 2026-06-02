import pytest
from django.test import Client
from django.urls import reverse
from accounts.models import User


# ── Tests pages accessibles ──────────────────────────────────────

@pytest.mark.django_db
def test_page_inscription():
    """La page d'inscription est accessible."""
    client = Client()
    response = client.get(reverse('auth:inscription'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_page_connexion():
    """La page de connexion est accessible."""
    client = Client()
    response = client.get(reverse('auth:connexion'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_page_accueil():
    """La page d'accueil est accessible."""
    client = Client()
    response = client.get('/')
    assert response.status_code == 200


# ── Tests inscription ─────────────────────────────────────────────

@pytest.mark.django_db
def test_inscription_cree_compte():
    """L'inscription crée un compte avec is_active=False."""
    client = Client()
    response = client.post(reverse('auth:inscription'), {
        'pseudo': 'testuser',
        'email': 'test@test.com',
        'password1': 'MotDePasse123!',
        'password2': 'MotDePasse123!',
    })
    assert response.status_code == 302
    user = User.objects.get(email='test@test.com')
    assert user.is_active is False
    assert user.pseudo == 'testuser'


@pytest.mark.django_db
def test_inscription_mdp_differents():
    """L'inscription échoue si les mots de passe sont différents."""
    client = Client()
    response = client.post(reverse('auth:inscription'), {
        'pseudo': 'testuser',
        'email': 'test@test.com',
        'password1': 'MotDePasse123!',
        'password2': 'AutreMotDePasse123!',
    })
    assert response.status_code == 200
    assert not User.objects.filter(email='test@test.com').exists()


# ── Tests connexion ───────────────────────────────────────────────

@pytest.mark.django_db
def test_connexion_compte_non_active():
    """La connexion est refusée si le compte n'est pas activé."""
    User.objects.create_user(
        username='test@test.com',
        email='test@test.com',
        password='MotDePasse123!',
        pseudo='testuser',
        is_active=False,
    )
    client = Client()
    response = client.post(reverse('auth:connexion'), {
        'username': 'test@test.com',
        'password': 'MotDePasse123!',
    })
    assert response.status_code == 200
    assert '_auth_user_id' not in client.session


@pytest.mark.django_db
def test_connexion_compte_active():
    """La connexion réussit si le compte est activé."""
    User.objects.create_user(
        username='test@test.com',
        email='test@test.com',
        password='MotDePasse123!',
        pseudo='testuser',
        is_active=True,
    )
    client = Client()
    response = client.post(reverse('auth:connexion'), {
        'username': 'test@test.com',
        'password': 'MotDePasse123!',
    })
    assert response.status_code == 302
    assert '_auth_user_id' in client.session


# ── Tests déconnexion ─────────────────────────────────────────────

@pytest.mark.django_db
def test_deconnexion():
    """La déconnexion fonctionne."""
    User.objects.create_user(
        username='test@test.com',
        email='test@test.com',
        password='MotDePasse123!',
        pseudo='testuser',
        is_active=True,
    )
    client = Client()
    client.login(username='test@test.com', password='MotDePasse123!')
    response = client.post(reverse('auth:deconnexion'))
    assert response.status_code == 302
    assert '_auth_user_id' not in client.session
