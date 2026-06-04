from django.db import models
from accounts.models import User


class Jeu(models.Model):
    nom = models.CharField(max_length=100)
    generation = models.IntegerField()
    plateforme = models.CharField(max_length=20)
    echanges_online = models.BooleanField(default=True)
    pokedex_regional = models.JSONField(default=list)
    exclusivites = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.nom


class Pokedex(models.Model):
    TYPE_VUE_CHOICES = [
        ('regional', 'Régional'),
        ('national', 'National'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=120)
    jeu = models.ForeignKey(Jeu, on_delete=models.CASCADE)
    type_vue = models.CharField(max_length=10, choices=TYPE_VUE_CHOICES, default='regional')
    mode_shiny = models.BooleanField(default=False)
    pokemon_statuses = models.JSONField(default=dict)
    shiny_statuses = models.JSONField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Règle : Capturé → automatiquement Vu
        for pokemon_id, statut in self.pokemon_statuses.items():
            if statut == 'capture':
                self.pokemon_statuses[pokemon_id] = 'capture'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.jeu.nom})"
