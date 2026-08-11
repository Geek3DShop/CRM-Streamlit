import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
clientes_path = os.getenv("CLIENTES_PATH")
custos_path = os.getenv("CUSTOS_PATH")

st.set_page_config(page_title="CRM Geek 3D Shop", layout="wide")

def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

clientes = pd.read_excel(clientes_path)

try:
    custos = pd.read_excel(custos_path)
    total_custos = custos["Custos"].sum()
except FileNotFoundError:
    total_custos = 0.0

receita_bruta = clientes["Valor da peça"].sum()
receita_liquida = receita_bruta - total_custos

col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
col1.title("CRM Geek 3D Shop")
col2.metric("Receita Bruta", formatar_reais(receita_bruta))
col3.metric("Custos", formatar_reais(total_custos))
col4.metric("Receita Líquida", formatar_reais(receita_liquida))

with st.expander("Adicionar Venda"):
    with st.form("nova_venda"):
        data = st.date_input("Data")
        acao = st.text_input("Ação")
        status = st.selectbox("Status", ["Contato", "Cliente em Potencial", "Cliente", "Parceiro"])
        nome = st.text_input("Nome")
        sobrenome = st.text_input("Sobrenome")
        contato = st.text_input("Telefone")
        peca = st.text_input("Peça")
        estagio_da_peca = st.selectbox("Estágio da peça", ["Não Iniciado", "Em progresso", "Concluído", "Perdido"])
        valor_da_peca = st.number_input("Valor da peça", min_value=0.0, step=0.01)

        confirmar = st.form_submit_button("Adicionar venda")

    if confirmar:
        clientes = pd.read_excel(clientes_path)
        nova_linha = {
            "Data": data,
            "Ação": acao,
            "Status": status,
            "Nome": nome,
            "Sobrenome": sobrenome,
            "Contato": contato,
            "Peça": peca,
            "Estágio da peça": estagio_da_peca,
            "Valor da peça": valor_da_peca,
        }
        clientes = pd.concat([clientes, pd.DataFrame([nova_linha])], ignore_index=True)
        clientes.to_excel(clientes_path, index=False)
        st.toast("Venda adicionada com sucesso!")
        st.rerun()

st.dataframe(clientes, width="stretch")