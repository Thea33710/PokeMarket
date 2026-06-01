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
