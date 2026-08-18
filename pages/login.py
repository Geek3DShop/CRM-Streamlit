import streamlit as st
from services.auth import authenticate

def login():
    st.title("🔐 CRM Geek 3D Shop")
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")