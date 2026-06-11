from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.liste_annonces, name='liste_annonces'),
    path('creer/', views.creer_annonce, name='creer_annonce'),
    path('autocomplete/', views.autocomplete_pokemon, name='autocomplete_pokemon'),
]
