# Variables par défaut
python := "python3"
venv_dir := ".venv"
bin_dir := venv_dir + "/bin"

# Recette par défaut (exécutée en tapant simplement `just`)
default: check test

# Crée l'environnement virtuel et installe toutes les dépendances de dev/test
setup: venv install-dev pre-commit-install

# Crée l'environnement virtuel Python (.venv) s'il n'existe pas
venv:
    @if [ ! -d "{{venv_dir}}" ]; then \
        echo "Création de l'environnement virtuel..."; \
        {{python}} -m venv {{venv_dir}}; \
    fi

# Installe les dépendances principales / production (requirements.txt)
install: venv
    {{bin_dir}}/pip install -r requirements.txt

# Installe les dépendances pour l'environnement de test et de dev local (requirements-dev.txt)
install-dev: venv
    {{bin_dir}}/pip install -r requirements-dev.txt

# Lance l'application Streamlit en local avec rechargement automatique à la sauvegarde
run:
    {{bin_dir}}/streamlit run app.py --server.runOnSave true

# Exécute les tests unitaires avec pytest
test:
    {{bin_dir}}/pytest

# Installe les hooks git pre-commit
pre-commit-install:
    {{bin_dir}}/pre-commit install

# Exécute manuellement tous les hooks git locaux sur l'ensemble des fichiers
hooks:
    {{bin_dir}}/pre-commit run --all-files

# Exécute toutes les vérifications du projet
check: hooks

# Nettoie les fichiers temporaires et les caches
clean:
    rm -rf .pytest_cache .ruff_cache __pycache__
