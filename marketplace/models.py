from django.db import models
from django.conf import settings
from pokedex.models import Jeu
import random


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
    cherche_genre = models.JSONField(null=True, blank=True)
    cherche_commentaire = models.TextField(null=True, blank=True)
    cherche_talents = models.JSONField(null=True, blank=True)
    # ex: ['Engrais', 'Protéen']

    # Ce que l'annonceur propose
    propositions = models.JSONField()

    # Comment échanger
    methode_echange = models.CharField(max_length=15, choices=METHODE_CHOICES)

    # État de l'annonce
    statut = models.CharField(
        max_length=15, choices=STATUT_CHOICES, default='ouverte'
    )

    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return (
            f"Annonce #{self.pk} — "
            f"Pokémon {self.pokemon_cherche_id} par {self.user.pseudo}"
        )


def generer_link_code():
    """Génère un Link Code à 8 chiffres au format XXXX-XXXX."""
    chiffres = random.randint(0, 99999999)
    code = f"{chiffres:08d}"
    return f"{code[:4]}-{code[4:]}"


class Echange(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ]

    METHODE_CHOICES = [
        ('link_code', 'Link Code'),
        ('code_ami', 'Code Ami Switch'),
    ]

    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name='echanges'
    )
    user_demandeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='echanges_demandes'
    )
    methode_utilisee = models.CharField(
        max_length=15,
        choices=METHODE_CHOICES
    )
    link_code = models.CharField(max_length=9, null=True, blank=True)
    link_code_expires_at = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(
        max_length=15,
        choices=STATUT_CHOICES,
        default='en_attente'
    )
    confirme_demandeur = models.BooleanField(default=False)
    confirme_annonceur = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Echange #{self.pk} — "
            f"{self.user_demandeur} sur annonce #{self.annonce_id}"
        )
