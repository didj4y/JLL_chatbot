import os
import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv

# Charger la clé API
load_dotenv()
MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
client = MistralClient(api_key=MISTRAL_API_KEY)

# Charger le contexte réseau depuis un fichier
with open("reseau_context.txt", "r", encoding="utf-8") as file:
    reseau_context = file.read()

# Titre de l'application
st.title("🔧 Chatbot Réseau - Spécialiste Cisco/Juniper")
st.markdown("Posez-moi une question technique sur les réseaux.")

# Initialiser l'historique de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        ChatMessage(role="assistant", content="Bonjour ! Je suis votre expert réseau. Posez-moi une question technique.")
    ]

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

# Champ de saisie pour l'utilisateur
if prompt := st.chat_input("Votre question..."):
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Préparer les messages pour Mistral AI avec le contexte réseau
    mistral_messages = [
        ChatMessage(role="system", content=f"""
        Tu es un expert réseau senior spécialisé dans Cisco, Juniper et Meraki.
        Voici des informations pour t'aider à répondre :
        {reseau_context}

        Règles :
        1. Réponds uniquement aux questions techniques réseau.
        2. Utilise des exemples de configuration CLI si nécessaire.
        3. Sois précis et pédagogique.
        """),
        *st.session_state.messages
    ]

    # Appeler l'API Mistral
    with st.spinner("Réflexion en cours..."):
        chat_response = client.chat(model="mistral-tiny", messages=mistral_messages)

    # Ajouter la réponse à l'historique
    assistant_response = chat_response.choices[0].message
    st.session_state.messages.append(assistant_response)

    # Afficher la réponse
    with st.chat_message("assistant"):
        st.markdown(assistant_response.content)
