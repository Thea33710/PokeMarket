from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'auth'

urlpatterns = [
    # Inscription et activation
    path('inscription/', views.inscription, name='inscription'),
    path('activer/<str:uidb64>/<str:token>/', views.activer_compte, name='activer'),

    # Connexion et déconnexion
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    # Reset mot de passe — Django fait tout !
    path('mdp-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/mdp_reset.html',
        email_template_name='accounts/mdp_reset_email.txt',
        success_url='/auth/mdp-reset/envoye/'
    ), name='mdp_reset'),

    path('mdp-reset/envoye/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/mdp_reset_envoye.html'
    ), name='mdp_reset_envoye'),

    path('mdp-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/mdp_reset_confirm.html',
        success_url='/auth/mdp-reset/termine/'
    ), name='mdp_reset_confirm'),

    path('mdp-reset/termine/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/mdp_reset_termine.html'
    ), name='mdp_reset_termine'),

    path('profil/', views.profil, name='profil'),
]
