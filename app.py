import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="CRM Geek 3D Shop", layout="wide")

st.title("CRM Geek 3D Shop")

path = os.getenv("CRM_PATH")
df = pd.read_excel(path)
df = df.dropna(axis=1, how="all")

st.dataframe(df, width="stretch")