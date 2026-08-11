import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
clientes_path = os.getenv("CRM_PATH")
custos_path = os.getenv("CUSTOS_PATH")

st.set_page_config(page_title="CRM Geek 3D Shop", layout="wide")

st.title("CRM Geek 3D Shop")
with st.expander("Adicionar Venda"):
    with st.form("nova_venda"):
        Data= st.date_input("Data")

        Ação= st.text_input("Ação")

        Status= st.selectbox( "Status", [ "Cliente", "Contato", "Parceiro", "Cliente em Potencial" ] )

        Nome= st.text_input("Nome")	

        Sobrenome= st.text_input("Sobrenome")

        Contato= st.text_input("Telefone")

        Peça= st.text_input("Peça")

        Estágio_da_peça= st.selectbox( "Estágio da peça", [ "Não Iniciado", "Em progresso", "Concluído", "Perdido" ] )

        Valor_da_peça= st.number_input("Valor da peça", min_value=0.0, step=0.01)

        confirmar= st.form_submit_button("Adicionar venda")

    if confirmar:
        df = pd.read_excel(clientes_path)
        nova_linha = { "Data": Data, "Ação": Ação, "Status": Status, 
                    "Nome": Nome, "Sobrenome": Sobrenome, 
                    "Contato": Contato, "Peça": Peça, 
                    "Estágio da peça": Estágio_da_peça, 
                    "Valor da peça": Valor_da_peça}
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        df.to_excel(clientes_path, index=False)
        st.success("Venda adicionada com sucesso!")

def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

df = pd.read_excel(clientes_path)
st.dataframe(df, width="stretch")

try:
    df_custos = pd.read_excel(custos_path)
    total_custos = df_custos["Custos"].sum()
except FileNotFoundError:
    total_custos = 0.0

receita_bruta = df["Valor da peça"].sum()
receita_liquida = receita_bruta - total_custos

col1, col2, col3 = st.columns(3)
col1.metric("Receita Bruta", brl(receita_bruta))
col2.metric("Custos", brl(total_custos))
col3.metric("Receita Líquida", brl(receita_liquida))