import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
ADM_USER = os.getenv("ADM_USER")
ADM_PASSWORD = os.getenv("ADM_PASSWORD")

def login():
    st.title("🔐 CRM Geek 3D Shop")
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):
        if username == ADM_USER and password == ADM_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

def authenticate(username, password):
    return username == ADM_USER and password == ADM_PASSWORD

def is_authenticated():
    return st.session_state.get("authenticated", False)

def logout():
    st.session_state["authenticated"] = False
    st.rerun()