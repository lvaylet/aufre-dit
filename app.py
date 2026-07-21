import os
from typing import cast

from google import genai
from google.genai import types
import httpx
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import streamlit as st

st.set_page_config(
    page_title="Chatbot FAQ - SGDF Aufrédy La Rochelle",
    page_icon="⚜️",
    layout="centered",
)

st.title("⚜️ Aufré-dit - La Rochelle")
st.caption(
    "Posez-moi vos questions sur les inscriptions, le matériel, les week-ends et les camps d'été."
)


class Settings(BaseSettings):
    """Configuration de l'application validée par Pydantic."""

    gemini_api_key: str = Field(min_length=1, validation_alias="GEMINI_API_KEY")
    faq_doc_url: str = Field(min_length=1, validation_alias="FAQ_DOC_URL")
    gemini_model: str = Field(
        default="gemini-3.5-flash", validation_alias="GEMINI_MODEL"
    )

    model_config = SettingsConfigDict(extra="ignore")


def load_settings() -> Settings:
    """Charge la configuration et affiche un message d'erreur clair si des variables sont manquantes."""
    api_key = os.getenv("GEMINI_API_KEY")
    doc_url = os.getenv("FAQ_DOC_URL")

    # Prise en charge des secrets Streamlit Cloud si non présent dans os.environ
    if not api_key and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        api_key = str(st.secrets["GEMINI_API_KEY"])
        os.environ["GEMINI_API_KEY"] = api_key
    if not doc_url and hasattr(st, "secrets") and "FAQ_DOC_URL" in st.secrets:
        doc_url = str(st.secrets["FAQ_DOC_URL"])
        os.environ["FAQ_DOC_URL"] = doc_url

    if not api_key or not doc_url:
        if not api_key:
            st.error(
                "💡 **Variable `GEMINI_API_KEY` manquante**\n\n"
                "Générez une clé sur [Google AI Studio](https://aistudio.google.com/) puis :\n\n"
                '* **En local** : Exécutez `export GEMINI_API_KEY="votre_cle_api"` dans votre terminal ou ajoutez la clé dans `.streamlit/secrets.toml`.\n'
                '* **Sur Streamlit Cloud** : Définissez `GEMINI_API_KEY = "votre_cle_api"` dans **Settings > Secrets**.'
            )
        if not doc_url:
            st.error(
                "💡 **Variable `FAQ_DOC_URL` manquante**\n\n"
                '* **En local** : Exécutez `export FAQ_DOC_URL="https://docs.google.com/document/d/..."` dans votre terminal ou ajoutez la clé dans `.streamlit/secrets.toml`.\n'
                '* **Sur Streamlit Cloud** : Définissez `FAQ_DOC_URL = "https://docs.google.com/document/d/..."` dans **Settings > Secrets**.'
            )
        st.stop()

    return Settings(
        gemini_api_key=api_key,
        faq_doc_url=doc_url,
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
    )


settings = load_settings()


def format_export_url(raw_url: str) -> str:
    """Formate l'URL du Google Doc pour s'assurer qu'elle se termine par /export?format=txt."""
    url = raw_url.strip()
    if "/export" in url:
        if "format=txt" not in url:
            base = url.split("/export")[0]
            return f"{base}/export?format=txt"
        return url
    if "/edit" in url:
        url = url.split("/edit")[0]
    url = url.rstrip("/")
    return f"{url}/export?format=txt"


@st.cache_data(ttl=3600)
def load_faq_document(url: str) -> str:
    """Télécharge le contenu texte à jour du Google Doc FAQ via httpx."""
    try:
        export_url = format_export_url(url)
        response = httpx.get(export_url, timeout=10.0, follow_redirects=True)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Erreur lors du chargement de la FAQ : {e}")
        return ""


@st.cache_data
def load_static_documents(folder_path: str = "static") -> str:
    """Charge le contenu texte de tous les fichiers .txt présents dans le dossier static."""
    documents: list[str] = []
    if os.path.exists(folder_path):
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".txt"):
                filepath = os.path.join(folder_path, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            documents.append(
                                f"=== DOCUMENT STATIC : {filename} ===\n{content}"
                            )
                except Exception as e:
                    st.error(
                        f"Erreur lors du chargement du document `{filename}` : {e}"
                    )
    return "\n\n".join(documents)


def build_system_instruction(faq_content: str, static_docs_content: str) -> str:
    """Construit la consigne système pour le modèle Gemini."""
    return f"""
Tu es l'assistant virtuel officiel du groupe Scouts et Guides de France (SGDF) - Aufrédy La Rochelle.
Ton objectif est de répondre aux questions des parents de manière claire, concise et bienveillante.

RÈGLES IMPÉRATIVES ET STRICTES DE FIDÉLITÉ ET DE CITATION :
1. Réponds EXCLUSIVEMENT et STRICTEMENT à partir des informations fournies dans les documents de référence ci-dessous.
2. N'invente aucune information, ne fais aucune supposition et n'utilise pas de connaissances externes.
3. Si la réponse ne se trouve PAS dans ces documents, tu DOIS répondre poliment que l'information n'est pas dans le guide et orienter le parent vers les interlocuteurs appropriés (Maîtrise/Chefs, Secrétariat/Trésorier ou Responsables de Groupe) conformément à la section 5 du document FAQ.
4. Adopte un ton Scout et Guides de France : chaleureux, constructif et serviable.
5. Indique TOUJOURS tes sources à la fin de chaque réponse pour montrer d'où viennent les informations : indique si les informations proviennent de la FAQ Google Doc et/ou des documents dans le dossier /static (en citant le nom exact du fichier, par exemple : Questions de Parents - Édition 2025-2026.txt).

--- DEBUT DE LA FAQ GOOGLE DOC DE RÉFÉRENCE ---
{faq_content}
--- FIN DE LA FAQ GOOGLE DOC DE RÉFÉRENCE ---

--- DEBUT DES DOCUMENTS STATIC DE RÉFÉRENCE ---
{static_docs_content}
--- FIN DES DOCUMENTS STATIC DE RÉFÉRENCE ---
"""


faq_content = load_faq_document(settings.faq_doc_url)
static_docs_content = load_static_documents("static")

# Initialisation du client Gemini API
client = genai.Client(api_key=settings.gemini_api_key)
system_instruction = build_system_instruction(faq_content, static_docs_content)

# Initialisation de l'historique de discussion
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Bonjour ! Je suis l'assistant du groupe SGDF Aufrédy La Rochelle. Posez-moi vos questions sur les inscriptions, la tenue, les week-ends ou les camps !",
        }
    ]

# Affichage de l'historique des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Saisie de l'utilisateur
if user_prompt := st.chat_input(
    "Ex: Quels sont les documents obligatoires pour l'inscription ?"
):
    # Affichage du message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Structuration de l'historique pour le SDK Gemini API
    contents: list[types.Content] = []
    for msg in st.session_state.messages[1:]:  # Omis le message d'accueil
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
        )

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans le guide FAQ..."):
            try:
                response = client.models.generate_content(
                    model=settings.gemini_model,
                    contents=cast(types.ContentListUnionDict, contents),
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.1,  # Température très basse pour garantir la fidélité au texte
                    ),
                )
                answer = response.text or ""
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as e:
                error_msg = f"Une erreur est survenue lors de la communication avec le service d'IA : {e}"
                st.error(error_msg)
