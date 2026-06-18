from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from pokedex.models import Jeu, PokemonCache
from .models import Annonce
from django.core.management import call_command


class AnnonceModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='thea',
            email='thea@test.com',
            password='test1234',
            pseudo='thea',
        )
        self.jeu = Jeu.objects.create(
            nom='Pokémon Écarlate & Violet',
            generation=9,
            plateforme='Switch',
            echanges_online=True,
            pokedex_regional=[906, 907, 908],
        )

    def _creer_annonce(self, **kwargs):
        defaults = dict(
            user=self.user,
            jeu=self.jeu,
            pokemon_cherche_id=906,
            propositions=[{'pokemon_id': 907}],
            methode_echange='link_code',
            expires_at=timezone.now() + timedelta(days=7),
        )
        defaults.update(kwargs)
        return Annonce.objects.create(**defaults)

    def test_creation_annonce(self):
        annonce = self._creer_annonce()
        self.assertEqual(annonce.statut, 'ouverte')
        self.assertEqual(annonce.pokemon_cherche_id, 906)

    def test_str_annonce(self):
        annonce = self._creer_annonce()
        self.assertIn('thea', str(annonce))

    def test_annonce_shiny(self):
        annonce = self._creer_annonce(cherche_shiny=True)
        self.assertTrue(annonce.cherche_shiny)

    def test_annonce_ivs(self):
        ivs = {'atk': 31, 'spe': 31}
        annonce = self._creer_annonce(cherche_ivs_min=ivs)
        self.assertEqual(annonce.cherche_ivs_min['atk'], 31)

    def test_annonce_propositions_json(self):
        annonce = self._creer_annonce(
            propositions=[{'pokemon_id': 907, 'shiny': True}]
        )
        self.assertEqual(annonce.propositions[0]['pokemon_id'], 907)
        self.assertTrue(annonce.propositions[0]['shiny'])

    def test_expiration_automatique(self):
        # Créer une annonce déjà expirée
        annonce = self._creer_annonce(
            expires_at=timezone.now() - timedelta(days=1)
        )
        self.assertEqual(annonce.statut, 'ouverte')
        call_command('expirer_annonces')
        annonce.refresh_from_db()
        self.assertEqual(annonce.statut, 'expiree')

    def test_expiration_ne_touche_pas_futures(self):
        # Créer une annonce pas encore expirée
        annonce = self._creer_annonce(
            expires_at=timezone.now() + timedelta(days=7)
        )
        call_command('expirer_annonces')
        annonce.refresh_from_db()
        self.assertEqual(annonce.statut, 'ouverte')


class AnnonceViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='thea',
            email='thea@test.com',
            password='test1234',
            pseudo='thea',
        )
        self.autre_user = User.objects.create_user(
            username='autre',
            email='autre@test.com',
            password='test1234',
            pseudo='autre',
        )
        self.jeu = Jeu.objects.create(
            nom='Pokémon Écarlate & Violet',
            generation=9,
            plateforme='Switch',
            echanges_online=True,
            pokedex_regional=[906, 907, 908],
        )
        PokemonCache.objects.create(
            pokemon_id=906,
            nom_fr='Poussacha',
            sprite_url='https://example.com/906.png',
            types=['plante'],
        )
        PokemonCache.objects.create(
            pokemon_id=907,
            nom_fr='Évoli',
            sprite_url='https://example.com/907.png',
            types=['normal'],
        )
        self.annonce = Annonce.objects.create(
            user=self.user,
            jeu=self.jeu,
            pokemon_cherche_id=906,
            propositions=[{'pokemon_id': 907}],
            methode_echange='link_code',
            expires_at=timezone.now() + timedelta(days=7),
        )

    def test_liste_annonces_non_connecte(self):
        response = self.client.get(reverse('marketplace:liste_annonces'))
        self.assertEqual(response.status_code, 302)

    def test_liste_annonces_connecte(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('marketplace:liste_annonces'))
        self.assertEqual(response.status_code, 200)

    def test_detail_annonce_connecte(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('marketplace:detail_annonce', args=[self.annonce.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_creer_annonce_non_connecte(self):
        response = self.client.get(reverse('marketplace:creer_annonce'))
        self.assertEqual(response.status_code, 302)

    def test_creer_annonce_post(self):
        self.client.force_login(self.user)
        self.client.post(reverse('marketplace:creer_annonce'), {
            'pokemon_cherche_id': 906,
            'cherche_shiny': False,
            'cherche_genre': [],
            'pokemon_propose_id': 907,
            'propose_shiny': False,
            'propose_genre': [],
            'methode_echange': 'link_code',
            'duree': 7,
        })
        self.assertEqual(Annonce.objects.count(), 2)

    def test_clore_annonce_proprietaire(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('marketplace:clore_annonce', args=[self.annonce.pk])
        )
        self.annonce.refresh_from_db()
        self.assertEqual(self.annonce.statut, 'terminee')

    def test_clore_annonce_autre_user(self):
        self.client.force_login(self.autre_user)
        response = self.client.post(
            reverse('marketplace:clore_annonce', args=[self.annonce.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_autocomplete_pokemon(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('marketplace:autocomplete_pokemon'),
            {'q': 'Pous'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Poussacha')
