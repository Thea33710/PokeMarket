# PokéMarket

> Pokédex tracker • Marketplace • Community Codes — Nintendo Switch only

![Django](https://img.shields.io/badge/Django-5.2-092E20) ![Python](https://img.shields.io/badge/Python-3.12-3776AB) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)

## C'est quoi ?

PokéMarket est une plateforme web communautaire pour joueurs Pokémon sur Nintendo Switch. Elle combine :
- 📖 Des Pokédex sauvegardables par partie
- 🤝 Une marketplace d'échanges structurée
- 🔢 Une page de codes communautaires standardisés

## Stack technique

- Backend : Django 5.2 + HTMX
- Base de données : PostgreSQL 16
- Hébergement : Render
- CI/CD : GitHub Actions

## Installation locale

```bash
git clone https://github.com/Thea33710/PokeMarket.git
cd PokeMarket
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # puis remplir les valeurs
python manage.py migrate
python manage.py runserver
```

## Sécurité

- Zéro donnée géographique collectée — jamais
- Link Codes jamais publics
- Code Ami Switch privé protégé par popup

## Statut

🚧 MVP en cours de développement — Phase 1 : Pokémon Écarlate & Violet
