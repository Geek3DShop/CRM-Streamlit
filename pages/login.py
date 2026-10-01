import time
import streamlit as st
from services.auth import authenticate

MAX_ATTEMPTS = 5
LOCKOUT_TIME = 60

def login():

    if "login_attempts" not in st.session_state:
        st.session_state["login_attempts"] = 0

    if "login_locked_until" not in st.session_state:
        st.session_state["login_locked_until"] = 0

    current_time = time.time()

    if current_time < st.session_state["login_locked_until"]:
        remaining = int(
            st.session_state["login_locked_until"] - current_time
        )

        st.title("🔐 CRM Geek 3D Shop")
        st.subheader("Login")

        st.error(
            f"Muitas tentativas. "
            f"Tente novamente em {remaining} segundos."
        )

        return

    st.title("🔐 CRM Geek 3D Shop")
    st.subheader("Login")

    username = st.text_input("Usuário")
    password = st.text_input(
        "Senha",
        type="password"
    )

    if st.button(
        "Entrar",
        use_container_width=True
    ):

        if authenticate(username, password):

            st.session_state["authenticated"] = True
            st.session_state["login_attempts"] = 0
            st.session_state["login_locked_until"] = 0

            st.rerun()

        else:

            st.session_state["login_attempts"] += 1

            attempts_left = (
                MAX_ATTEMPTS
                - st.session_state["login_attempts"]
            )

            if st.session_state["login_attempts"] >= MAX_ATTEMPTS:

                st.session_state["login_locked_until"] = (
                    time.time() + LOCKOUT_TIME
                )

                st.error(
                    "Muitas tentativas inválidas. "
                    "Login bloqueado por 60 segundos."
                )

            else:
                st.error(
                    f"Usuário ou senha incorretos. "
                    f"Tentativas restantes: {attempts_left}"
                )