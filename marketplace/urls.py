from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.liste_annonces, name='liste_annonces'),
    path('creer/', views.creer_annonce, name='creer_annonce'),
    path(
        'autocomplete/',
        views.autocomplete_pokemon,
        name='autocomplete_pokemon'
    ),
    path('talents/', views.talents_pokemon, name='talents_pokemon'),
    path('mes-echanges/', views.mes_echanges, name='mes_echanges'),
    path('<int:pk>/', views.detail_annonce, name='detail_annonce'),
    path('<int:pk>/clore/', views.clore_annonce, name='clore_annonce'),
    path(
        'annonces/<int:annonce_id>/proposer/',
        views.proposer_echange,
        name='proposer_echange'
    ),
    path(
        'echanges/<int:pk>/',
        views.detail_echange,
        name='detail_echange'
    ),
    path(
        'echanges/<int:pk>/confirmer/',
        views.confirmer_echange,
        name='confirmer_echange'
    ),
    path(
        'echanges/<int:pk>/accepter/',
        views.accepter_echange,
        name='accepter_echange'
    ),
    path(
        'echanges/<int:pk>/refuser/',
        views.refuser_echange,
        name='refuser_echange'
    ),
]
