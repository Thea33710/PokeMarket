from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),
    path(
        'codes-communautaires/',
        views.codes_communautaires,
        name='codes_communautaires'
    ),
]
