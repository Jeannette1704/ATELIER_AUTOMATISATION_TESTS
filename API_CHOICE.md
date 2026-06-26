# Choix de l'API pour l'Atelier

Dans le cadre de cet atelier d'automatisation des tests, j'ai choisi l'API publique **ZenQuotes**.

- **URL de l'API :** `https://zenquotes.io/api/random`
- **Description :** Cette API permet de récupérer des citations inspirantes ou philosophiques de manière aléatoire au format JSON.
- **Critères de validation appliqués dans le test :**
  1. Le code de statut HTTP doit être égal à `200` (Succès).
  2. La réponse reçue doit être une liste non vide contenant la structure attendue (`q` pour la citation, `a` pour l'auteur).
