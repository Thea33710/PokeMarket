# 💡 Idées à explorer — PokéMarket

Ce fichier note les idées identifiées pendant le développement,
à étudier pour une phase future.

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
**Phase suggérée :** Phase 2 ou refonte MVP si le temps le permet

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
**Phase suggérée :** Phase 2

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
**Phase suggérée :** Phase 2

---

*(à compléter au fil du développement)*
