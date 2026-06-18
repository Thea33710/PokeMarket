from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from pokedex.models import Jeu, Pokedex, PokemonCache


class TestModelePokedex(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testeur',
            email='test@test.com',
            pseudo='testeur',
            password='testpass123',
        )
        self.jeu = Jeu.objects.create(
            nom='Pokémon Écarlate & Violet',
            generation=9,
            plateforme='Switch',
            echanges_online=True,
            pokedex_regional=[906, 907, 908],
        )
        self.pokedex = Pokedex.objects.create(
            user=self.user,
            nom='Test Pokédex',
            jeu=self.jeu,
            pokemon_statuses={},
        )

    def test_statut_initial_non_vu(self):
        """Un Pokémon non marqué est non_vu par défaut."""
        statut = self.pokedex.pokemon_statuses.get('906', 'non_vu')
        self.assertEqual(statut, 'non_vu')

    def test_capture_sauvegarde(self):
        """On peut marquer un Pokémon comme capturé."""
        self.pokedex.pokemon_statuses['906'] = 'capture'
        self.pokedex.save()
        self.pokedex.refresh_from_db()
        self.assertEqual(self.pokedex.pokemon_statuses['906'], 'capture')

    def test_vu_sauvegarde(self):
        """On peut marquer un Pokémon comme vu."""
        self.pokedex.pokemon_statuses['906'] = 'vu'
        self.pokedex.save()
        self.pokedex.refresh_from_db()
        self.assertEqual(self.pokedex.pokemon_statuses['906'], 'vu')

    def test_plusieurs_statuts_independants(self):
        """Les statuts de différents Pokémon sont indépendants."""
        self.pokedex.pokemon_statuses['906'] = 'capture'
        self.pokedex.pokemon_statuses['907'] = 'vu'
        self.pokedex.pokemon_statuses['908'] = 'non_vu'
        self.pokedex.save()
        self.pokedex.refresh_from_db()
        self.assertEqual(self.pokedex.pokemon_statuses['906'], 'capture')
        self.assertEqual(self.pokedex.pokemon_statuses['907'], 'vu')
        self.assertEqual(self.pokedex.pokemon_statuses['908'], 'non_vu')


class TestPokemonCache(TestCase):

    def test_creation_cache(self):
        """On peut créer une entrée de cache."""
        cache = PokemonCache.objects.create(
            pokemon_id=906,
            nom_fr='Poussacha',
            sprite_url='https://example.com/906.png',
            types=['plante'],
        )
        self.assertEqual(cache.nom_fr, 'Poussacha')
        self.assertEqual(cache.types, ['plante'])

    def test_pokemon_id_unique(self):
        """Deux entrées avec le même pokemon_id sont impossibles."""
        PokemonCache.objects.create(
            pokemon_id=906,
            nom_fr='Poussacha',
            sprite_url='https://example.com/906.png',
            types=['plante'],
        )
        with self.assertRaises(Exception):
            PokemonCache.objects.create(
                pokemon_id=906,
                nom_fr='Doublon',
                sprite_url='https://example.com/906.png',
                types=['plante'],
            )


class TestVueMarquer(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testeur2',
            email='test2@test.com',
            pseudo='testeur2',
            password='testpass123',
            is_active=True,
        )
        self.jeu = Jeu.objects.create(
            nom='Pokémon Écarlate & Violet Test',
            generation=9,
            plateforme='Switch',
            echanges_online=True,
            pokedex_regional=[906],
        )
        self.pokedex = Pokedex.objects.create(
            user=self.user,
            nom='Test',
            jeu=self.jeu,
            pokemon_statuses={},
            mode_shiny=True,
            shiny_statuses={},
        )
        PokemonCache.objects.create(
            pokemon_id=906,
            nom_fr='Poussacha',
            sprite_url='https://example.com/906.png',
            types=['plante'],
        )
        self.client.force_login(self.user)

    def test_marquer_vu(self):
        """Marquer un Pokémon comme vu."""
        url = reverse('pokedex:marquer', args=[self.pokedex.pk, 906, 'vu'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.pokedex.refresh_from_db()
        self.assertEqual(self.pokedex.pokemon_statuses['906'], 'vu')

    def test_marquer_capture(self):
        """Marquer un Pokémon comme capturé."""
        url = reverse('pokedex:marquer', args=[self.pokedex.pk, 906, 'capture'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.pokedex.refresh_from_db()
        self.assertEqual(self.pokedex.pokemon_statuses['906'], 'capture')

    def test_decocher_capture_repasse_vu(self):
        """Décocher capturé repasse à vu."""
        self.pokedex.pokemon_statuses['906'] = 'capture'
        self.pokedex.save()
        url = reverse('pokedex:marquer', args=[self.pokedex.pk, 906, 'capture'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.pokedex.refresh_from_db()
        self.assertEqual(self.pokedex.pokemon_statuses['906'], 'vu')

    def test_marquer_shiny(self):
        """Marquer un Pokémon comme shiny."""
        url = reverse('pokedex:marquer', args=[self.pokedex.pk, 906, 'shiny'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.pokedex.refresh_from_db()
        self.assertTrue(self.pokedex.shiny_statuses['906'])

    def test_marquer_non_connecte(self):
        """Un utilisateur non connecté est redirigé."""
        self.client.logout()
        url = reverse('pokedex:marquer', args=[self.pokedex.pk, 906, 'vu'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)


class TestVuesPokedex(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testeur3',
            email='test3@test.com',
            pseudo='testeur3',
            password='testpass123',
        )
        self.jeu = Jeu.objects.create(
            nom='Pokémon Écarlate & Violet',
            generation=9,
            plateforme='Switch',
            echanges_online=True,
            pokedex_regional=[906, 907],
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
        self.pokedex = Pokedex.objects.create(
            user=self.user,
            nom='Mon Pokédex',
            jeu=self.jeu,
            pokemon_statuses={},
        )

    def test_liste_pokedex_non_connecte(self):
        response = self.client.get(reverse('pokedex:liste'))
        self.assertEqual(response.status_code, 302)

    def test_liste_pokedex_connecte(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pokedex:liste'))
        self.assertEqual(response.status_code, 200)

    def test_creer_pokedex_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pokedex:creer'))
        self.assertEqual(response.status_code, 200)

    def test_creer_pokedex_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('pokedex:creer'), {
            'nom': 'Nouveau Pokédex',
            'jeu': self.jeu.pk,
            'type_vue': 'regional',
            'mode_shiny': False,
        })
        self.assertEqual(Pokedex.objects.filter(user=self.user).count(), 2)

    def test_detail_pokedex_connecte(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('pokedex:detail', args=[self.pokedex.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_pokedex_non_connecte(self):
        response = self.client.get(
            reverse('pokedex:detail', args=[self.pokedex.pk])
        )
        self.assertEqual(response.status_code, 302)
