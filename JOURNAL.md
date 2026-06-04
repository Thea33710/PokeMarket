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

## Session 2 (suite) — GitHub Actions + Tests

### Ce qu'on a fait
- Créé .github/workflows/ci.yml → pipeline CI/CD
- Créé pytest.ini
- Installé pytest, pytest-django, pytest-cov, flake8
- Écrit 8 tests unitaires Auth (93% couverture)
- Corrigé les erreurs flake8
- GitHub Actions passe au vert ✅

### Problèmes rencontrés
- pytest exit code 5 → aucun test trouvé → solution : créer les tests !
- permission denied to create database → solution : ALTER USER pokemarket_user CREATEDB
- Node.js 20 deprecation warning → pas grave, juste un avertissement

### État actuel
- CI/CD GitHub Actions actif et vert ✅
- 8 tests passent, couverture 93% ✅

### Prochaines étapes
- Déploiement sur Render
- Sprint review

## Session 2 (suite) — Déploiement Render

### Ce qu'on a fait
- Installé gunicorn + whitenoise
- Configuré settings.py pour la production
- Créé build.sh
- Créé la base de données PostgreSQL sur Render
- Créé le Web Service sur Render
- Déployé le site en production ✅

### Problèmes rencontrés
- "Cannot GET /" → ALLOWED_HOSTS ne contenait pas la bonne URL Render
  → Solution : ajouter 'pokemarket-r00f.onrender.com' dans ALLOWED_HOSTS
- "Not Found" après correction → cache du navigateur
  → Solution : ouvrir un onglet privé

### État actuel
- Site en ligne sur https://pokemarket-r00f.onrender.com ✅
- CI/CD GitHub Actions vert ✅
- 8 tests, 93% couverture ✅

### Sprint 1 — TERMINÉ ! 🎉

## Sprint Review — Sprint 1

### Ce qui a bien marché
- Django + PostgreSQL connectés
- Flux auth complet (inscription, email, activation, connexion, reset mdp)
- GitHub Actions vert
- Site déployé sur Render ✅

### Ce qui a pris du temps
- Droits PostgreSQL (2 fois !)
- GitHub Actions rouge au premier essai (pas de tests)
- URL Render différente de ce qu'on attendait
- Cache navigateur

### Leçons apprises
- Donner CREATEDB à pokemarket_user dès le début
- Tester en onglet privé après déploiement
- Vérifier l'URL exacte Render avant ALLOWED_HOSTS

### Métriques Sprint 1
- Tâches complétées : 8/8 ✅
- Tests : 8 tests, 93% couverture ✅
- Site en ligne : https://pokemarket-r00f.onrender.com ✅

## Note — Base de données Render
- BDD gratuite expire après 90 jours
- Solution : supprimer + recréer une nouvelle BDD gratuite
- Mettre à jour DATABASE_URL dans les variables Render
- Relancer migrate → tout repart !
- Date limite approximative : fin août 2026

## Session 3 — Sprint 2 — Modèles Jeu + Pokédex + seed S/V

### Ce qu'on a fait
- Créé l'app Django `pokedex`
- Écrit les modèles `Jeu` et `Pokédex` avec leurs champs complets
- Appliqué les migrations ✅
- Enregistré les modèles dans l'admin Django
- Créé la commande de seed `seed_sv`
- Installé `requests`
- Seedé les données Scarlet & Violet depuis PokéAPI : 400 Pokémon du Pokédex Paldea ✅
- Commité et pushé sur `dev`

### Problèmes rencontrés
- `ModuleNotFoundError: No module named 'requests'` → solution : pip install requests

### État actuel
- Branche active : dev
- Modèles Jeu + Pokédex en base ✅
- 400 Pokémon Paldea seedés ✅

### Prochaines étapes (Sprint 2 suite)
- Vues et templates Pokédex (liste, création, marquage)
