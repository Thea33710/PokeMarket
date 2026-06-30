from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle utilisateur personnalisé pour PokéMarket."""

    pseudo = models.CharField(max_length=80, unique=True)
    pokemon_avatar_id = models.IntegerField(null=True, blank=True)
    avatar_couleur = models.CharField(max_length=7, default='#7030a0')
    code_ami_switch = models.CharField(max_length=15, null=True, blank=True)

    VISIBILITE_CHOICES = [
        ('public', 'Public'),
        ('prive', 'Privé'),
        ('non_renseigne', 'Non renseigné'),
    ]
    visibilite_code_ami = models.CharField(
        max_length=13,
        choices=VISIBILITE_CHOICES,
        default='prive'
    )

    nb_echanges = models.IntegerField(default=0)

    def __str__(self):
        return self.pseudo
