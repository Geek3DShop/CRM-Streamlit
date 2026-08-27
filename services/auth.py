import os
import streamlit as st
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
from argon2 import PasswordHasher


load_dotenv()

ADM_USER = os.getenv("ADM_USER")
ADM_PASSWORD_HASH = os.getenv("ADM_PASSWORD_HASH")

password_hasher = PasswordHasher()


def authenticate(username, password):
    if not ADM_USER or not ADM_PASSWORD_HASH:
        return False

    if username != ADM_USER:
        return False

    try:
        return password_hasher.verify(
            ADM_PASSWORD_HASH,
            password
        )

    except VerifyMismatchError:
        return False


def is_authenticated():
    return st.session_state.get("authenticated", False)


def logout():
    st.session_state["authenticated"] = False
    st.rerun()