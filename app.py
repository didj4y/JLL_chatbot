import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

client = OpenAI(
    api_key=GEMINI_API_KEY, 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Charger le contexte réseau
with open("reseaucontext.txt", "r", encoding="utf-8") as file:
    reseaucontext = file.read()

st.title("Chatbot JLL - Support")
st.markdown("Quel est votre problème ?")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Pose moi ta question"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    gemini_messages = [
        {"role": "system", "content": f"Tu es un expert en informatique senior spécialisé... Voici des informations pour t’aider à répondre : {reseaucontext} Règles : 1. ..."},
    ]

    gemini_messages += st.session_state.messages

    with st.spinner("Réflexion en cours..."):
        response = client.chat.completions.create(
            model="gemini-2.5-pro",  # ou gemini-2.5-flash selon ton abonnement
            messages=gemini_messages
        )
        assistant_response = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
