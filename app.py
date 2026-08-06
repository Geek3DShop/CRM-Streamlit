import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

st.title("CRM Geek 3D Shop")

path = os.getenv("CRM_PATH")
df = pd.read_excel(path)
st.dataframe(df)