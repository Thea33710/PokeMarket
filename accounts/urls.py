from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('activer/<str:uidb64>/<str:token>/', views.activer_compte, name='activer'),
]
