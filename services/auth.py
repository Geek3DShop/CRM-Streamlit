import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
CRM_USER = os.getenv("CRM_USER")
CRM_PASSWORD = os.getenv("CRM_PASSWORD")

def login():
    st.title("🔐 CRM Geek 3D Shop")
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):
        if username == CRM_USER and password == CRM_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

def authenticate(username, password):
    return username == CRM_USER and password == CRM_PASSWORD

def is_authenticated():
    return st.session_state.get("authenticated", False)

def logout():
    st.session_state["authenticated"] = False
    st.rerun()