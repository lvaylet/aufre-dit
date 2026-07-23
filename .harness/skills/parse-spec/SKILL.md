---
name: parse-spec
description: Analyse une spécification Markdown SDLC pour en extraire le plan d'exécution, la liste des tâches, les modèles de données et les critères d'acceptation.
---

# Instruction de la Skill `parse-spec`

Lorsqu'un agent invoque cette skill avec le chemin d'un fichier `.md` dans `.harness/specs/` :

1. **Extraction du périmètre** :
   - Identifier les éléments `In-Scope` et `Out-of-Scope`.
2. **Parsing des User Stories & Critères d'acceptation** :
   - Lister toutes les User Stories (`US-X`) et leurs critères `AC-X.Y` (Given/When/Then).
3. **Identification des composants à modifier/créer** :
   - Relever les fichiers cibles et les modèles Pydantic définis dans la section Architecture.
4. **Restitution** :
   - Produire un tableau récapitulatif des tâches pour l'Agent Orchestrateur.
