# 💡 Idées à explorer — PokéMarket

Ce fichier note les idées identifiées pendant le développement,
à explorer après le MVP.

---

## 🔄 Refonte du système d'annonces

**Idée :** Remplacer le système actuel (1 Pokémon cherché + 1 proposé)
par deux listes séparées :
- 📋 **Liste "je veux"** — tous les Pokémon que l'annonceur souhaite recevoir
- 🎁 **Liste "je donne"** — tous les Pokémon que l'annonceur accepte de donner

**Pourquoi c'est intéressant :**
- Plus naturel pour les joueurs qui ont beaucoup de stock
- Permet de matcher plusieurs besoins en une seule annonce
- Réduit le nombre d'annonces dupliquées

**Complexité :** Moyenne — changerait le modèle Annonce et l'interface

---

## 💬 Système de propositions sur les annonces

**Idée :** Permettre à un visiteur de faire une contre-proposition
sur une annonce existante.

**Exemple concret :**
- L'annonceur veut un Rosélia contre son Briochien
- Le visiteur n'a pas de Rosélia mais a un Rosébouton
- Il peut proposer "je te donne mon Rosébouton contre ton Briochien"
- L'annonceur peut accepter ou refuser

**Pourquoi c'est intéressant :**
- Plus flexible que le système strict cherche/propose
- Crée une vraie dynamique de négociation communautaire
- Correspond mieux à la réalité des échanges Pokémon

**Complexité :** Moyenne — nécessite un modèle Proposition lié à Annonce
+ notifications pour l'annonceur

---

## 📊 Système de demande de précisions sur les IVs/talents/nature

**Idée :** Si un chercheur veut absolument des IVs/talents/nature précis
mais que l'annonce ne les spécifie pas, afficher une popup/formulaire
pour qu'il puisse demander ces précisions à l'annonceur.

**Exemple :**
- L'annonce ne précise pas les IVs
- Le visiteur veut absolument 31 en Attaque
- Il peut envoyer une demande de précisions à l'annonceur

**Complexité :** Moyenne — lié au système de propositions

---

## 🎮 Jeux possédés sur le profil utilisateur

**Idée :** Ajouter un champ `jeux_possedes` sur le modèle User pour
que l'utilisateur puisse indiquer quels jeux il possède.

**Utilité :**
- Pré-sélectionner automatiquement le bon jeu dans le formulaire d'annonce
- Personnaliser l'expérience marketplace selon les jeux possédés

**À faire :**
- Ajouter `jeux_possedes = models.ManyToManyField(Jeu, blank=True)` dans User
- Créer la migration
- Ajouter le champ sur la page profil (Sprint 4)

---

## 🔍 Filtres marketplace — côté "je donne"

**Idée :** Ajouter un deuxième mode de recherche dans la marketplace :
- Côté "je cherche" (actuel) — je cherche un Pokémon à recevoir
- Côté "je donne" — je cherche quelqu'un à qui donner mon Pokémon

**Note :** Le côté "je donne" ressemble plus à une enchère —
nécessiterait peut-être une discussion ou une négociation entre joueurs.

---

## 🔤 Normalisation des accents dans les recherches

**Idée :** Permettre de chercher "evoli" et trouver "Évoli",
"poussacha" et trouver "Poussacha", etc.
Appliquer partout : marketplace, pokédex, autocomplete.

**Solution :** normalize('NFD').replace(/[\u0300-\u036f]/g, '')

---

## ⚙️ Préférence méthode d'échange par utilisateur

**Idée :** Ajouter une préférence "méthode d'échange préférée" (Link Code / Code Ami Switch)
dans les réglages du profil utilisateur.
Si l'annonce accepte les deux, utiliser la préférence de l'utilisateur.
Par défaut : Link Code (pas de données personnelles partagées).

**Solution :** Champ `methode_preferee` sur le modèle `User` + case à cocher dans les réglages profil.

---

## 💡 Bandeau informatif Code Ami Switch non renseigné

**Idée :** Afficher un bandeau discret (jaune/orange) sur les pages marketplace
si l'utilisateur connecté n'a pas renseigné son Code Ami Switch.
Message : "Tu n'as pas renseigné ton Code Ami Switch. Les échanges par Code Ami
ne seront pas disponibles pour tes annonces. [Renseigner mon code ami →]"
Le bandeau disparaît automatiquement si le code est renseigné.
Ne pas afficher si l'utilisateur n'a volontairement pas renseigné son code
(ajouter une option "ne plus afficher").

**Solution envisagée :** Vérification dans le contexte template +
bandeau conditionnel dans `base.html` ou dans les templates marketplace.

---

*(à compléter au fil du développement)*
