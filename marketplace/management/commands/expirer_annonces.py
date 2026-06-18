from django.core.management.base import BaseCommand
from django.utils import timezone
from marketplace.models import Annonce


class Command(BaseCommand):
    help = 'Passe les annonces expirées en statut expiree'

    def handle(self, *args, **kwargs):
        annonces_expirees = Annonce.objects.filter(
            statut='ouverte',
            expires_at__lt=timezone.now()
        )
        total = annonces_expirees.count()
        annonces_expirees.update(statut='expiree')
        self.stdout.write(self.style.SUCCESS(
            f'✅ {total} annonce(s) expirée(s) mise(s) à jour.'
        ))
