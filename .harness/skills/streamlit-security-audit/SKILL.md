---
name: streamlit-security-audit
description: Réalise un contrôle de sécurité ciblé sur le code Python/Streamlit pour détecter les failles XSS, les fuites de secrets et l'assainissement des entrées.
---

# Instruction de la Skill `streamlit-security-audit`

Cette skill passe au peigne fin les fichiers Streamlit (`app.py`, etc.) :

1. **Recherche de `unsafe_allow_html=True`** :
   - Rechercher toutes les occurrences de `unsafe_allow_html=True`.
   - Vérifier si du contenu provenant d'une entrée utilisateur (`st.text_input`, etc.) y est injecté directement sans échappement HTML.
2. **Recherche de secrets stockés en dur** :
   - Rechercher les expressions correspondant à des jetons d'API (ex: `AIzaSy...`, `sk-...`, mots de passe).
   - S'assurer que le code utilise `st.secrets` ou `os.getenv(...)`.
3. **Validation des entrées utilisateur** :
   - Vérifier que toutes les saisies utilisateurs sont validées par des schémas Pydantic avant traitement.
4. Produire un bilan `PASS` / `FAIL` avec recommandations.
