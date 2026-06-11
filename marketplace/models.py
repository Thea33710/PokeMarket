from django.db import models
from django.conf import settings
from pokedex.models import Jeu


class Annonce(models.Model):

    METHODE_CHOICES = [
        ('link_code', 'Link Code'),
        ('code_ami', 'Code Ami Switch'),
        ('les_deux', 'Les deux'),
    ]

    STATUT_CHOICES = [
        ('ouverte', 'Ouverte'),
        ('en_attente', 'En attente'),
        ('terminee', 'Terminée'),
        ('expiree', 'Expirée'),
    ]

    DUREE_CHOICES = [
        (7, '7 jours'),
        (14, '14 jours'),
        (30, '30 jours'),
    ]

    # Qui a créé l'annonce
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='annonces'
    )

    # Quel jeu
    jeu = models.ForeignKey(
        Jeu,
        on_delete=models.CASCADE,
        related_name='annonces'
    )

    # Pokémon recherché
    pokemon_cherche_id = models.IntegerField()

    # Précisions optionnelles sur le Pokémon cherché
    cherche_shiny = models.BooleanField(null=True, blank=True)
    cherche_nature = models.CharField(max_length=20, null=True, blank=True)
    cherche_ivs_min = models.JSONField(null=True, blank=True)
    cherche_talent = models.CharField(max_length=10, null=True, blank=True)
    cherche_genre = models.CharField(max_length=10, null=True, blank=True)
    cherche_commentaire = models.TextField(null=True, blank=True)

    # Ce que l'annonceur propose
    propositions = models.JSONField()

    # Comment échanger
    methode_echange = models.CharField(max_length=15, choices=METHODE_CHOICES)

    # État de l'annonce
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='ouverte')

    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"Annonce #{self.pk} — Pokémon {self.pokemon_cherche_id} par {self.user.pseudo}"
