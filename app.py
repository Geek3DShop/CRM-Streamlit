import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
clientes_path = os.getenv("CLIENTES_PATH")
custos_path = os.getenv("CUSTOS_PATH")

st.set_page_config(page_title="CRM Geek 3D Shop",  page_icon="💰", layout="wide")

st.title("CRM Geek 3D Shop")
st.caption("Controle de clientes, vendas, custos e lucro")

def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

clientes = pd.read_excel(clientes_path)

try:
    custos = pd.read_excel(custos_path)
    total_custos = custos["Custos"].sum()
except FileNotFoundError:
    total_custos = 0.0

def carrega_dados():
    if(clientes_path):
        df = pd.read_excel(clientes_path)
    else: 
        df = pd.DataFrame(columns=[
           "Data",
            "Ação",
            "Status",
            "Nome",
            "Sobrenome",
            "Contato",
            "Peça",
            "Estágio da peça",
            "Valor da peça",
            "Receita Bruta",
            "Custos",
            "Receita Líquida" 
        ])
    return df

def salvar_dados(df):
    df.to_excel(clientes_path, index=False)

df = carrega_dados()
colunas_numericas = [
        "Valor da peça",
        "Receita Bruta",
        "Custos",
        "Receita Líquida"
    ]

for coluna in colunas_numericas:
    if coluna in df.columns:
        df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce"
            ).fillna(0)

total_vendas =len(df)
receita_bruta = df["Receita Bruta"].sum()

custos = df["Custos"].sum()

receita_liquida = receita_bruta - custos

if receita_bruta > 0:
     margem_lucro = (
            receita_liquida / receita_bruta
    ) * 100
else: 
    margem_lucro = 0
    
col1, col2, col3, col4, col5 = st.columns( [2, 2, 2, 2, 2])
with col1:
        st.metric("🛒 Vendas", total_vendas)
    
with col2:
            st.metric("💵 Receita Bruta", f"R$ {receita_bruta:,.2f}")
with col3:
            st.metric("💸 Custos",f"R$ {custos:,.2f}")
with col4:
            st.metric("💰 Receita Líquida",f"R$ {receita_liquida:,.2f}")
with col5:
            st.metric("📈 Margem", f"R$ {margem_lucro:,.2f}")

st.divider()

with st.expander("➕ Adicionar Venda"):
        with st.form("nova_venda"):
            st.subheader("Dados da venda")
            col1, col2, col3 = st.columns(3)
            with col1: 
                Data = st.date_input("Data", value=pd.Timestamp.today().date())

                Ação = st.text_input("Ação")

                Status	= st.selectbox( "Status", [ "Cliente", "Contato", "Parceiro", "Cliente em Potencial" ] )
            with col2:
                Nome = st.text_input("Nome")	

                Sobrenome	= st.text_input("Sobrenome")

                Contato	= st.text_input("Telefone")
            with col3:

                Peça	= st.text_input("Peça")

                Estágio_da_peça	 = st.selectbox( "Estágio da peça", [ "Não Iniciado", "Em progresso", "Concluído", "Perdido" ] )

                Valor_da_peça = st.number_input("Valor da peça (R$)", min_value=0.0, step=0.01, format="%.2f")

            st.divider()

            confirmar = st.form_submit_button("💾 Adicionar venda")

        if confirmar:
            Receita_Bruta = Valor_da_peça
            Custos = 0.0
            Receita_Líquida = Receita_Bruta - Custos  

            nova_linha = {
                "Data": Data,
                "Ação": Ação,
                "Status": Status,
                "Nome": Nome,
                "Sobrenome": Sobrenome,
                "Contato": Contato,
                "Peça": Peça,
                "Estágio da peça": Estágio_da_peça,
                "Valor da peça": Valor_da_peça,
                "Receita Bruta": Receita_Bruta,
                "Custos": Custos,
                "Receita Líquida": Receita_Líquida
            }

            df = pd.concat([
                df,  pd.DataFrame([nova_linha])
            ], ignore_index=True)

            salvar_dados(df)

            st.success(f"Venda de {Nome} adicionada com sucesso!")
            st.rerun()
st.dataframe(clientes, width="stretch")