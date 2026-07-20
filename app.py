import os
import requests
import streamlit as st
from google import genai
from google.genai import types

# URL d'exportation au format texte brut du Google Doc FAQ public
DOC_URL = "https://docs.google.com/document/d/1PtDzEbEDFFKPgl_T8rz3PCiLrU8X2Fh2qqsZQqEOgt0/export?format=txt"

st.set_page_config(
    page_title="Chatbot FAQ - SGDF Aufrédy La Rochelle",
    page_icon="⚜️",
    layout="centered"
)

st.title("⚜️ Aufré-dit - La Rochelle")
st.caption("Posez-moi vos questions sur les inscriptions, le matériel, les week-ends et les camps d'été.")

@st.cache_data(ttl=3600)
def load_faq_document() -> str:
    """Télécharge le contenu texte à jour du Google Doc FAQ."""
    try:
        response = requests.get(DOC_URL, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Erreur lors du chargement de la FAQ : {e}")
        return ""

faq_content = load_faq_document()

# Vérification de la présence de la clé API Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.info("💡 **Configuration requise** : Veuillez définir la clé d'environnement `GEMINI_API_KEY` (dans les Secrets Streamlit Cloud ou localement).")
    st.stop()

# Configuration du modèle (supporte GEMINI_MODEL en variable d'environnement)
model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# Initialisation du client Gemini API
client = genai.Client(api_key=api_key)

system_instruction = f"""
Tu es l'assistant virtuel officiel du groupe Scouts et Guides de France (SGDF) - Aufrédy La Rochelle.
Ton objectif est de répondre aux questions des parents de manière claire, concise et bienveillante.

RÈGLES IMPÉRATIVES ET STRICTES DE FIDÉLITÉ :
1. Réponds EXCLUSIVEMENT et STRICTEMENT à partir des informations fournies dans le document FAQ ci-dessous.
2. N'invente aucune information, ne fais aucune supposition et n'utilise pas de connaissances externes.
3. Si la réponse ne se trouve PAS dans le document FAQ, tu DOIS répondre poliment que l'information n'est pas dans le guide et orienter le parent vers les interlocuteurs appropriés (Maîtrise/Chefs, Secrétariat/Trésorier ou Responsables de Groupe) conformément à la section 5 du document.
4. Adopte un ton Scout et Guides de France : chaleureux, constructif et serviable.

--- DEBUT DU DOCUMENT FAQ DE RÉFÉRENCE ---
{faq_content}
--- FIN DU DOCUMENT FAQ DE RÉFÉRENCE ---
"""

# Initialisation de l'historique de discussion
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Bonjour ! Je suis l'assistant du groupe SGDF Aufrédy La Rochelle. Posez-moi vos questions sur les inscriptions, la tenue, les week-ends ou les camps !"
        }
    ]

# Affichage de l'historique des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Saisie de l'utilisateur
if user_prompt := st.chat_input("Ex: Quels sont les documents obligatoires pour l'inscription ?"):
    # Affichage du message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Structuration de l'historique pour le SDK Gemini API
    contents = []
    for msg in st.session_state.messages[1:]:  # Omis le message d'accueil
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans le guide FAQ..."):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.1,  # Température très basse pour garantir la fidélité au texte
                    )
                )
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Une erreur est survenue lors de la communication avec le service d'IA : {e}"
                st.error(error_msg)

