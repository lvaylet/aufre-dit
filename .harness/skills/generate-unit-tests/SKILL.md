---
name: generate-unit-tests
description: Génère les squelettes et cas de test unitaires Pytest pour un composant ou un service Python donné.
---

# Instruction de la Skill `generate-unit-tests`

Lors de l'appel à cette skill avec un fichier source Python (ex: `services/search.py`) :

1. **Analyse du fichier source** :
   - Identifier toutes les classes, méthodes publiques et fonctions.
   - Relever leurs types de paramètres et de retour.
2. **Génération de la matrice de test** :
   - Écrire un cas de test nominal pour chaque fonction.
   - Écrire un cas de test aux limites (entrées `None`, chaînes vides, types invalides).
   - Injecter des mocks (`unittest.mock.MagicMock` ou `pytest.fixture`) pour tout appel réseau ou SDK externe (ex: API GenAI).
3. **Format du fichier de sortie** :
   - Créer ou mettre à jour le fichier `test_<nom_du_fichier>.py`.
