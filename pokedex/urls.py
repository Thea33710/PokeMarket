from django.urls import path
from . import views

app_name = 'pokedex'

urlpatterns = [
    path('', views.liste_pokedex, name='liste'),
    path('creer/', views.creer_pokedex, name='creer'),
    path('<int:pk>/', views.detail_pokedex, name='detail'),
]
