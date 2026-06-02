# Journal de bord — PokéMarket

## Session 1 — Sprint 1 — Fondations

### Ce qu'on a fait
- Cloné le repo GitHub sur la tour
- Créé l'environnement virtuel (venv)
- Installé Django 5.2.14, psycopg2-binary, python-dotenv
- Créé le projet Django avec django-admin
- Testé le serveur local (fusée Django visible ✅)
- Configuré PostgreSQL (base + utilisateur + droits)
- Créé le fichier .env avec les infos de connexion
- Connecté Django à PostgreSQL
- Créé la branche dev sur GitHub
- Ajouté README.md et .env.example
- Créé l'app accounts + modèle User personnalisé
- Appliqué toutes les migrations ✅

### Problèmes rencontrés

**Problème 1 — Django 6.0.5 installé par erreur**
- Cause : pip a installé une version qui n'existe pas encore
- Solution : désinstallé et réinstallé avec "django>=5.0,<6.0"

**Problème 2 — Permission denied sur PostgreSQL**
- Cause : pokemarket_user n'avait pas les droits sur le schema public
- Solution : sudo -u postgres psql → \c pokemarket → GRANT ALL ON SCHEMA public TO pokemarket_user

**Problème 3 — max_length trop petit sur visibilite_code_ami**
- Cause : "non_renseigne" fait 13 caractères, max_length était à 12
- Solution : changé max_length=12 → max_length=13 dans models.py

**Problème 4 — InconsistentMigrationHistory**
- Cause : on avait fait migrate avant de créer le User personnalisé
- Solution : DROP DATABASE + CREATE DATABASE + rejouer migrate depuis zéro

### État actuel
- Branche active : dev
- Django + PostgreSQL connectés ✅
- Modèle User personnalisé créé ✅
- Repo GitHub : https://github.com/Thea33710/PokeMarket.git

### Prochaines étapes (Sprint 1 suite)
- Inscription + confirmation email + is_active
- Connexion + déconnexion + reset mot de passe
- Templates de base (base.html + HTMX + CSS responsive)
- GitHub Actions CI/CD
- Déploiement Render

## Session 2 — Sprint 1 — Inscription + Auth

### Ce qu'on a fait
- Configuré l'email en mode console (affiche dans le terminal)
- Créé accounts/forms.py → formulaire d'inscription
- Créé accounts/views.py → vues inscription, activation, connexion, déconnexion
- Créé accounts/urls.py → routes /auth/...
- Créé l'app core pour la page d'accueil
- Créé les templates : base.html, inscription.html, connexion.html, accueil.html
- Testé le flux complet : inscription → email → activation → connexion ✅

### Problèmes rencontrés
Aucun ! Tout a fonctionné du premier coup 🎉

### État actuel
- Branche active : dev
- Flux d'authentification complet et fonctionnel ✅
- Templates de base créés ✅

### Prochaines étapes
- Connexion + déconnexion + reset mot de passe (US-03)
- Templates de base (base.html + HTMX + CSS responsive)
- GitHub Actions CI/CD

## Session 2 (suite) — Reset mot de passe

### Ce qu'on a fait
- Ajouté les 4 URLs de reset mot de passe dans accounts/urls.py
- Créé les 4 templates : mdp_reset, mdp_reset_envoye, mdp_reset_confirm, mdp_reset_termine
- Créé le template email mdp_reset_email.txt

### Problèmes rencontrés
- http:// en double dans le lien email
  → Solution : enlever le http:// manuel, {{ protocol }} le met déjà tout seul

### État actuel
- Reset mot de passe complet et fonctionnel ✅

### Prochaines étapes
- Templates de base HTMX + CSS responsive
- GitHub Actions CI/CD
- Déploiement Render
