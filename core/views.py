from django.shortcuts import render


def accueil(request):
    """Page d'accueil."""
    return render(request, 'core/accueil.html')
