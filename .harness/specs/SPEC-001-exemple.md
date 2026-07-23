# SPEC-001 : Module de Restitution et Filtrage des FAQs par Catégorie

## 1. Contexte & Objectif

- **Description synthétique** : Ajouter un composant de sélection et filtrage des questions/réponses de la FAQ par catégorie (ex: Inscriptions, Cotisations, Camp) dans l'interface Streamlit.
- **Utilisateurs cibles** : Parents et jeunes adhérents du groupe SGDF Aufrédy La Rochelle.
- **Périmètre (In-Scope)** :
  - [ ] Sélecteur de catégorie dans la barre latérale (`st.sidebar.selectbox`).
  - [ ] Filtrage automatique de la liste des FAQs affichées.
  - [ ] Validation du modèle de catégorie via Pydantic.
- **Hors-Périmètre (Out-of-Scope)** :
  - Modification du moteur de réponse LLM / RAG sous-jacent.

## 2. Spécifications Fonctionnelles & User Stories

### US-1 : Filtrage dynamique des FAQs

En tant que visiteur, je veux pouvoir filtrer les questions par thème afin de trouver rapidement l'information qui me concerne.

- **Critères d'Acceptation** :
  - **AC-1.1** : **GIVEN** que l'utilisateur ouvre l'application, **WHEN** il sélectionne une catégorie (ex: "Cotisations"), **THEN** seules les questions associées à cette catégorie apparaissent dans la vue principale.
  - **AC-1.2** : **GIVEN** que la catégorie "Toutes" est sélectionnée, **WHEN** l'affichage se met à jour, **THEN** l'intégralité des FAQs est présentée.

---

## 3. Architecture Technique & Modèles de Données

- **Composants impactés** :
  - `app.py`
- **Modèle Pydantic** :

  ```python
  from enum import Enum
  from pydantic import BaseModel

  class CategoryEnum(str, Enum):
      ALL = "Toutes"
      INSCRIPTION = "Inscriptions"
      COTISATION = "Cotisations"
      CAMP = "Camps & Sorties"

  class FAQFilter(BaseModel):
      category: CategoryEnum = CategoryEnum.ALL
  ```

---

## 4. Requis Non-Fonctionnels & Sécurité

- **Typage** : Mode strict Pyright (`typeCheckingMode = "strict"`).
- **Sécurité** : Filtrage côté serveur, aucun échappement HTML brut (`unsafe_allow_html=False`).

---

## 5. Matrice de Tests Attendu

- [ ] `test_faq_filter_enum_validation` : Vérifie la validité des valeurs de catégories.
- [ ] `test_filter_faq_by_category` : Vérifie le filtrage correct de la liste des FAQs.

---

## 6. Journal des Portes de Qualité (Quality Gates)

- [ ] `just check` passe sans erreur.
- [ ] 100% des tests unitaires Pytest réussis.
