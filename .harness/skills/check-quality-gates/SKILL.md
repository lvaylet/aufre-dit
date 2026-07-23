---
name: check-quality-gates
description: Exécute la suite complète de vérifications de qualité de code (Ruff, Pyright, Pytest) via la commande `just check`.
---

# Instruction de la Skill `check-quality-gates`

Lorsque cette skill est appelée :

1. Exécutez la commande `just check` via l'outil `run_command` dans le répertoire racine du projet.
2. Analyser le code de retour et la sortie standard :
   - Si `just check` se termine avec succès (code 0) : Renvoyer un statut `QUALITY_GATES_PASSED`.
   - En cas d'erreur :
     - Si Ruff échoue : Renvoyer la liste des règles violées et les lignes impactées.
     - Si Pyright échoue : Renvoyer les erreurs de typage strict avec leurs emplacements exacts (`file:///path/to/file#Lxx`).
     - Si Pytest échoue : Renvoyer le nom du test échoué et sa trace d'erreur (`traceback`).
3. Formater la réponse sous forme de rapport synthétique pour l'Orchestrateur ou l'Agent QA.
