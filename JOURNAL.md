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

## Session 3 (suite) — Intégration PokéAPI + cache local

### Ce qu'on a fait
- Créé le modèle `PokemonCache` (pokemon_id, nom_fr, sprite_url, types)
- Appliqué la migration ✅
- Créé la commande `cache_pokeapi`
- Rempli le cache : 400 Pokémon, 0 erreurs ✅
- Mis à jour les GitHub Actions vers Node.js 24 (checkout@v5, setup-python@v6)
- Corrigé les erreurs flake8 (imports inutilisés, variables non utilisées)
- CI verte ✅

### Problèmes rencontrés
- GitHub Actions rouge → erreurs flake8 dans seed_sv.py, views.py, tests.py
  → Solution : nettoyer les imports et variables inutilisés

### État actuel
- Cache PokéAPI complet : 400 Pokémon avec noms FR, sprites, types ✅
- CI GitHub Actions verte ✅

## Session 3 (suite) — Vue liste + création Pokédex

### Ce qu'on a fait
- Créé les vues `liste_pokedex`, `creer_pokedex`, `detail_pokedex`
- Créé `pokedex/forms.py` avec `PokedexForm`
- Créé `pokedex/urls.py` et branché dans `pokemarket/urls.py`
- Créé les templates : `liste_pokedex.html`, `creer_pokedex.html`, `detail_pokedex.html`
- Testé en local : liste, création, affichage des 400 Pokémon avec sprites FR ✅

### Problèmes rencontrés
- Import `Jeu` inutilisé dans views.py → erreur flake8 → supprimé

### État actuel
- Vue liste Pokédex ✅
- Vue création Pokédex ✅
- Vue détail avec 400 Pokémon, noms FR, sprites, types ✅

## Session 3 (suite) — Marquage HTMX

### Ce qu'on a fait
- Créé la vue `marquer_pokemon` avec 3 actions : vu, capture, shiny
- Créé le fragment `pokemon_card.html` avec icônes 👁️ 🔴 ✨
- Ajouté le CSS pour les statuts et icônes (actif/grisé)
- Marquage fonctionne sans rechargement de page grâce à HTMX ✅
- Règle : capturé → décocher repasse à vu (pas non_vu)
- Shiny uniquement visible si mode_shiny activé sur le Pokédex

### Problèmes rencontrés
- Swap HTMX ne se voyait pas → CSS manquant pour statut-vu/non_vu/capture
- Cycle non_vu→vu→capture ne correspondait pas au besoin → remplacé par boutons indépendants
- Import HttpResponse inutilisé → erreur flake8 → supprimé

### État actuel
- Marquage HTMX complet et fonctionnel ✅
- CI verte ✅

## Session 3 (suite) — Barre de progression + mode shiny

### Ce qu'on a fait
- Ajouté CSS pour la barre de progression (dégradé violet)
- Ajouté compteur shiny sous la barre si mode_shiny activé
- Mise à jour en temps réel via HTMX hx-swap-oob ✅
- Créé fragment `marquer_response.html` pour combiner carte + barre

### Problèmes rencontrés
- hx-swap-oob dans le fragment carte → barre dupliquée dans chaque carte
  → Solution : template séparé `marquer_response.html` retourné par la vue

### État actuel
- Barre de progression mise à jour sans rechargement ✅
- Compteur shiny fonctionnel ✅
- CI verte ✅

## Session 3 (suite) — Filtres Pokédex + recherche

### Ce qu'on a fait
- Ajouté barre de filtres : recherche par nom/numéro, filtre type, filtre statut, filtre shiny
- Filtres en JavaScript pur (pas de rechargement de page)
- Compteur de résultats affichés
- Statut simplifié : capturé / non capturé (pas besoin de vu/non vu)
- Types disponibles calculés dynamiquement depuis le cache

### Problèmes rencontrés
- Aucun !

### État actuel
- Filtres fonctionnels ✅
- CI verte ✅

## Session 3 (suite) — Tests unitaires Pokédex + Sprint Review

### Ce qu'on a fait
- Écrit 11 tests unitaires : modèles, cache, vues marquage
- Corrigé : CREATEDB manquant, username requis, force_login pour auth email
- 11/11 tests passent ✅
- CI verte ✅

### Problèmes rencontrés
- CREATEDB manquant → ALTER USER pokemarket_user CREATEDB
- create_user nécessite username (AbstractUser) → ajouté
- client.login() ne fonctionne pas avec auth email → remplacé par force_login

### Sprint 2 — TERMINÉ 🎉

## Sprint Review — Sprint 2

### Ce qui a bien marché
- Modèles Jeu + Pokédex + PokemonCache ✅
- Seed 400 Pokémon Paldea depuis PokéAPI ✅
- Cache local noms FR, sprites, types ✅
- Marquage HTMX sans rechargement ✅
- Barre de progression temps réel ✅
- Filtres type, statut, recherche ✅
- 11 tests, CI verte ✅

### Ce qui a pris du temps
- hx-swap-oob mal placé → barre dupliquée dans chaque carte
- force_login vs client.login avec auth email

### Métriques Sprint 2
- Cartes complétées : 6/6 ✅
- Tests Pokédex : 11 tests ✅
- CI verte ✅

## Session 4 — Sprint 3 — Modèle Annonce

### Ce qu'on a fait
- Créé l'app Django `marketplace` avec startapp
- Ajouté `marketplace` dans INSTALLED_APPS
- Créé le modèle `Annonce` avec tous les champs :
  pokemon_cherche_id, précisions optionnelles (shiny, nature, ivs_min,
  talent, genre, commentaire), propositions (JSONField),
  methode_echange, statut, expires_at
- Migration créée et appliquée ✅
- Modèle enregistré dans l'admin Django
- 19 tests passent, rien de cassé ✅
- Pushé sur dev

### Problèmes rencontrés
Aucun !

### État actuel
- Branche active : dev
- Modèle Annonce en base ✅

### Prochaines étapes (Sprint 3 suite)
- Formulaire création annonce (US-09)

## Session 4 (suite) — Sprint 3 — Formulaire création annonce (US-09)

### Ce qu'on a fait
- Créé `marketplace/forms.py` avec AnnonceForm complète
- Autocomplete par nom de Pokémon via HTMX
- Champs obligatoires : shiny (case à cocher), genre
- Champs optionnels : nature, talent, commentaire, IVs (6 stats 0-31)
- Mêmes champs pour le Pokémon proposé
- Vue `creer_annonce` et `liste_annonces` avec noms et sprites
- Filtre templatetag `get_item` pour accéder au cache Pokémon
- Vue `autocomplete_pokemon` pour la recherche par nom
- Corrigé erreurs flake8
- CI verte ✅

### Problèmes rencontrés
- Autocomplete ne fonctionnait plus → name="q" manquant sur les inputs
- Clic sur résultat ne fonctionnait plus → IDs des champs cachés incorrects
- flake8 : variable annonce inutilisée, indentation choices, blank lines

### Idées notées dans IDEES.md
- Système de listes "je veux / je donne"
- Système de contre-propositions sur les annonces
- Popup demande de précisions IVs/talents/nature

### Prochaines étapes
- Liste + détail annonces + filtres marketplace (US-10)

## Session 4 (suite) — Sprint 3 — Améliorations formulaire annonce

### Ce qu'on a fait
- Ajouté talents dans PokemonCache (JSONField) + migration
- Mis à jour cache_pokeapi pour récupérer les noms FR des talents
- Relancé le cache : 400 Pokémon avec talents en français ✅
- Talents dynamiques : chargement automatique via HTMX selon le Pokémon sélectionné
- Genre changé en cases à cocher (MultipleChoiceField) — optionnel pour cherché, optionnel pour proposé
- cherche_genre changé en JSONField dans le modèle Annonce + migration
- Ajouté cherche_talents (JSONField) dans le modèle Annonce + migration
- Affichage talents et nature du proposé dans la liste des annonces
- Corrigé erreurs flake8
- CI verte ✅

### Problèmes rencontrés
- cherche_genre sauvegardé comme string au lieu de liste → changé en JSONField
- Migration impossible car vieilles données invalides → vidé les annonces puis migré
- flake8 : espaces sur lignes vides, trop de lignes vides

### Idées notées dans IDEES.md
- Jeux possédés sur le profil utilisateur (ManyToManyField)

### État actuel
- Formulaire création annonce complet ✅
- Liste annonces avec tous les détails ✅
- CI verte ✅

### Prochaines étapes
- Liste + détail annonces + filtres marketplace (US-10)

## Session 4 (suite) — Sprint 3 — Liste + détail annonces + filtres (US-10)

### Ce qu'on a fait
- Page détail annonce avec tous les champs (cherché + proposé + méthode)
- Lien "Voir le détail →" sur chaque carte de la liste
- Filtres JavaScript : recherche par nom (proposé uniquement), shiny proposé, méthode d'échange
- Attributs data- sur les cartes pour les filtres
- Compteur d'annonces affichées
- Correction : recherche filtre sur le Pokémon proposé (celui qu'on reçoit)
- Correction : filtre shiny sur le Pokémon proposé
- CI verte ✅

### Problèmes rencontrés
- Deux divs annonce-card imbriquées → compteur affichait 2 au lieu de 1
- dataset.noms_propose → camelCase en JS → dataset.nomsPropose
- noms_annonces non défini → oublié dans le return de la vue

### Idées notées dans IDEES.md
- Filtres marketplace côté "je donne"
- Normalisation des accents dans toutes les recherches

### Prochaines étapes
- Clôture + expiration automatique annonces (7/14/30j)

## Session 5 — Sprint 3 — Clôture + expiration automatique annonces

### Ce qu'on a fait
- Vue `clore_annonce` : l'annonceur peut fermer son annonce manuellement
- Template `confirmer_cloture.html` avec confirmation avant clôture
- Bouton "Clore l'annonce" visible uniquement par l'annonceur sur la page détail
- Commande de gestion `expirer_annonces` : passe les annonces expirées en statut `expiree`
- CI verte ✅

### Problèmes rencontrés
- flake8 : 1 ligne vide au lieu de 2 avant clore_annonce

### État actuel
- Clôture manuelle ✅
- Expiration automatique ✅

### Prochaines étapes
- Tests unitaires Marketplace + sprint review (dernière carte Sprint 3)

## Session 5 (suite) — Sprint 3 — Tests + Sprint Review

### Ce qu'on a fait
- 15 tests unitaires marketplace : modèle, vues, expiration, accès anonyme
- 6 tests supplémentaires pokédex : vues liste, créer, détail
- Corrigé clore_annonce : get_object_or_404 au lieu de get()
- 40 tests passent, couverture 83% ✅

### Problèmes rencontrés
- test_clore_annonce_autre_user → DoesNotExist au lieu de 404
  → Solution : get_object_or_404
- flake8 : variables response inutilisées dans les tests

### Sprint 3 — TERMINÉ 🎉

## Sprint Review — Sprint 3

### Ce qui a bien marché
- Formulaire annonce complet avec autocomplete et talents dynamiques ✅
- Filtres marketplace fonctionnels ✅
- Page détail annonce ✅
- Clôture manuelle + expiration automatique ✅
- 40 tests, 83% couverture ✅

### Ce qui a pris du temps
- Genre en JSONField (migration bloquée par vieilles données)
- dataset camelCase en JavaScript (noms_propose → nomsPropose)
- Double div annonce-card dans le template

### Métriques Sprint 3
- Cartes complétées : 5/5 ✅
- Tests : 40 tests, 83% couverture ✅
- CI verte ✅

### Prochaines étapes
- Sprint 4 : Mise en relation (Echange model, Link Code, Code Ami, profil)

## Sprint 4

### Modèle Echange + Link Code (US-11)
- Ajout modèle `Echange` dans `marketplace/models.py`
- Fonction `generer_link_code()` format XXXX-XXXX
- Vue `proposer_echange` : création échange avec Link Code, expiration 24h
- Vue `detail_echange` : page Link Code visible uniquement aux deux joueurs
- Bouton "Proposer un échange" dans `detail_annonce.html`
- setup.cfg créé pour exclure les migrations de flake8

### Flux Code Ami Switch + popup avertissement (US-12, US-13)
- Adaptation de `proposer_echange` : Link Code par défaut, Code Ami uniquement si méthode exclusive
- Popup avertissement avant affichage du Code Ami Switch (bouton "J'ai compris")
- Message si Code Ami non public ou non renseigné
- Bandeau informatif sur liste_annonces, detail_annonce et creer_annonce si Code Ami non renseigné

### Confirmation bilatérale échange + incrément nb_échanges
- Champs `confirme_demandeur` et `confirme_annonceur` ajoutés sur le modèle Echange
- Vue `confirmer_echange` : confirmation bilatérale, incrément nb_echanges, clôture annonce
- Bouton de confirmation dans detail_echange
- ⚠️ À vérifier : l'annonceur n'a pas encore accès à ses échanges en cours
  (dépend de la page profil/tableau de bord — Sprint 4)
