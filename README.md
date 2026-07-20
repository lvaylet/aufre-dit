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

### Méthode standard (virtualenv)

1. Créez et activez un environnement virtuel Python (`venv`) :
   * **Linux / macOS** :

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   * **Windows** :

     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```

2. Installez les dépendances (développement inclus) :

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Définissez les variables d'environnement, soit dans le terminal :

   ```bash
   export GEMINI_API_KEY="votre_cle_api_ici"
   export FAQ_DOC_URL="https://docs.google.com/document/d/1PtDzEbEDFFKPgl_T8rz3PCiLrU8X2Fh2qqsZQqEOgt0"
   ```

   Soit dans le fichier `.streamlit/secrets.toml` :

   ```toml
   GEMINI_API_KEY = "votre_cle_api_ici"
   FAQ_DOC_URL = "https://docs.google.com/document/d/1PtDzEbEDFFKPgl_T8rz3PCiLrU8X2Fh2qqsZQqEOgt0"
   ```

4. Lancez l'application Streamlit :

   ```bash
   streamlit run app.py
   ```

### Méthode NixOS / Nix

Si vous utilisez NixOS ou le gestionnaire de paquets Nix, un environnement reproductible complet est disponible (via `shell.nix` et `flake.nix`). Il fournit nativement Python 3, Streamlit, les outils de linting/tests (Ruff, Pyright, Pre-commit) et `just`.

1. **Activez l'environnement de développement** :
   * Avec les Flakes (recommandé) :

     ```bash
     nix develop
     ```

   * Sans Flakes (classique) :

     ```bash
     nix-shell
     ```

   * Avec `direnv` (chargement automatique à l'entrée dans le répertoire) :

     ```bash
     direnv allow
     ```

2. **Définissez les variables d'environnement** :
   Exportez `GEMINI_API_KEY` et `FAQ_DOC_URL` dans votre terminal comme indiqué dans la méthode standard.

3. **Exécutez l'application** :
   * Lancement direct :

     ```bash
     streamlit run app.py
     ```

   * Lancement via `just` (en indiquant d'utiliser les paquets de la Nix shell plutôt que le `.venv`) :

     ```bash
     just --set bin_dir "" run
     ```

---

## 📄 Extraction de contenu PDF (`static/`)

L'application charge automatiquement tous les fichiers `.txt` présents dans le dossier `static/` afin d'enrichir la base de connaissances du chatbot.

Pour ajouter un document PDF et générer le fichier `.txt` correspondant dans le dossier `static/` :

### Méthode 1 : Avec `pdftotext` (Recommandé)

`pdftotext` (issu de la suite Poppler) est l'outil le plus rapide et le plus efficace.

1. **Installation** (si l'outil n'est pas disponible) :
   * **Linux (Debian / Ubuntu)** : `sudo apt install poppler-utils`
   * **macOS** : `brew install poppler`

2. **Extraction** :

   ```bash
   pdftotext static/votre_document.pdf static/votre_document.txt
   ```

   *Exemple avec le guide PDF "Questions de Parents - Édition 2025-2026"* :

   ```bash
   pdftotext "static/Questions de Parents - Édition 2025-2026.pdf" "static/Questions de Parents - Édition 2025-2026.txt"
   ```

### Méthode 2 : Avec Python (`pypdf`)

1. Installez `pypdf` dans votre environnement virtuel :

   ```bash
   pip install pypdf
   ```

2. Générez le fichier `.txt` via la commande Python suivante :

   ```bash
   python3 -c "from pypdf import PdfReader; reader = PdfReader('static/votre_document.pdf'); text = '\n'.join([p.extract_text() for p in reader.pages if p.extract_text()]); open('static/votre_document.txt', 'w', encoding='utf-8').write(text)"
   ```

---

## 🧪 Tests Unitaires & Pre-commit

Pour installer le hook git localement et exécuter les vérifications (linter, formateur, pyright, pytest) :

```bash
pre-commit install
pre-commit run --all-files
```

---

## 🌐 Hébergement Gratuit et Simple (Streamlit Community Cloud)

1. Publiez ce projet sur votre compte **GitHub** (dépôt public ou privé).
2. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io/) avec votre compte GitHub.
3. Cliquez sur **New app** et sélectionnez votre dépôt `aufre-dit`.
4. Dans les **Advanced settings** / **Secrets**, ajoutez votre clé API et l'URL de votre FAQ :

   ```toml
   GEMINI_API_KEY = "votre_cle_api_ici"
   FAQ_DOC_URL = "https://docs.google.com/document/d/1PtDzEbEDFFKPgl_T8rz3PCiLrU8X2Fh2qqsZQqEOgt0"
   ```

   > **Note sur `FAQ_DOC_URL`** : L'application formate automatiquement l'URL du Google Doc. Vous pouvez utiliser n'importe laquelle de ces 4 formes :
   > * `https://docs.google.com/document/d/<ID>`
   > * `https://docs.google.com/document/d/<ID>/`
   > * `https://docs.google.com/document/d/<ID>/edit`
   > * `https://docs.google.com/document/d/<ID>/export?format=txt`

5. Cliquez sur **Deploy**. Votre chatbot sera disponible gratuitement sur une URL de type `https://aufre-dit.streamlit.app` accessible par tous les parents.
