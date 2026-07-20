# ⚜️ Chatbot FAQ - SGDF Aufrédy La Rochelle

Ce projet propose un chatbot interactif dédié aux parents du groupe SGDF Aufrédy La Rochelle, répondant **uniquement** à partir des informations centralisées dans le Google Doc FAQ public du groupe.

## 🎯 Fonctionnalités

* **Fidélité stricte au document** : Le chatbot s'appuie exclusivement sur la FAQ Google Doc du groupe et renvoie vers les contacts appropriés si l'information est absente.
* **Mise à jour automatique** : Le document est relu directement depuis son URL d'exportation au format texte brut (`export?format=txt`). Toute modification du Google Doc par l'équipe d'animation s'applique au chatbot sans aucune ré-installation.
* **100% Gratuit** : Hébergement gratuit sur Streamlit Community Cloud et utilisation du quota gratuit de Gemini (ex: Gemini 3.5 Flash) via Google AI Studio.

---

## 🚀 Préqurequis & Obtention de la Clé API Gemini (Gratuit)

1. Rendez-vous sur [Google AI Studio](https://aistudio.google.com/).
2. Connectez-vous avec votre compte Google.
3. Cliquez sur **Get API key** puis **Create API key**.
4. Copiez la clé d'API générée.

---

## 💻 Test en Local

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

2. Définissez les variables d'environnement :
   ```bash
   export GEMINI_API_KEY="votre_cle_api_ici"
   export FAQ_DOC_URL="https://docs.google.com/document/d/1PtDzEbEDFFKPgl_T8rz3PCiLrU8X2Fh2qqsZQqEOgt0"
   ```

3. Lancez l'application Streamlit :
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Tests Unitaires

Pour lancer les tests unitaires (par exemple la validation du formatage des URL d'export du Google Doc) :

```bash
python -m unittest test_app.py
```

---

## 🌐 Hébergement Gratuit et Simple (Streamlit Community Cloud)

1. Publiez ce projet sur votre compte **GitHub** (dépôt public ou privé).
2. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io/) avec votre compte GitHub.
3. Cliquez sur **New app** et sélectionnez votre dépôt `sgdf-chatbot`.
4. Dans les **Advanced settings** / **Secrets**, ajoutez votre clé API et l'URL de votre FAQ :
   ```toml
   GEMINI_API_KEY = "votre_cle_api_ici"
   FAQ_DOC_URL = "https://docs.google.com/document/d/1PtDzEbEDFFKPgl_T8rz3PCiLrU8X2Fh2qqsZQqEOgt0"
   ```

   > **Note sur `FAQ_DOC_URL`** : L'application formate automatiquement l'URL du Google Doc. Vous pouvez utiliser n'importe laquelle de ces 4 formes :
   > - `https://docs.google.com/document/d/<ID>`
   > - `https://docs.google.com/document/d/<ID>/`
   > - `https://docs.google.com/document/d/<ID>/edit`
   > - `https://docs.google.com/document/d/<ID>/export?format=txt`

5. Cliquez sur **Deploy**. Votre chatbot sera disponible gratuitement sur une URL de type `https://sgdf-chatbot.streamlit.app` accessible par tous les parents.
