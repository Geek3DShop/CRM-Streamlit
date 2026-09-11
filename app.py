import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
clientes_path = os.getenv("CLIENTES_PATH")
custos_path = os.getenv("CUSTOS_PATH")

def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def carrega_dados():
    if os.path.exists(clientes_path):
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
            "Receita Líquida",
        ])
    return df

def salvar_dados(df):
    df.to_excel(clientes_path, index=False)

st.set_page_config(page_title="CRM Geek 3D Shop", page_icon="💰", layout="wide")

if not clientes_path:
    st.error("A variável CLIENTES_PATH não está definida no arquivo .env.")
    st.stop()

st.title("CRM Geek 3D Shop")
st.caption("Controle de clientes, vendas, custos e lucro")

df = carrega_dados()

colunas_numericas = [
    "Valor da peça",
    "Receita Bruta",
    "Custos",
    "Receita Líquida",
]

for coluna in colunas_numericas:
    if coluna in df.columns:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce").fillna(0)

if custos_path and os.path.exists(custos_path):
    custos = pd.read_excel(custos_path)
    total_custos = pd.to_numeric(custos["Custos"], errors="coerce").sum()
else:
    total_custos = 0.0

total_vendas = len(df)
receita_bruta = df["Valor da peça"].sum()
receita_liquida = receita_bruta - total_custos

if receita_bruta > 0:
    margem_lucro = (receita_liquida / receita_bruta) * 100
else:
    margem_lucro = 0.0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🛒 Vendas", total_vendas)
with col2:
    st.metric("💵 Receita Bruta", formatar_reais(receita_bruta))
with col3:
    st.metric("💸 Custos", formatar_reais(total_custos))
with col4:
    st.metric("💰 Receita Líquida", formatar_reais(receita_liquida))
with col5:
    st.metric("📈 Margem", f"{margem_lucro:.2f}%".replace(".", ","))

st.divider()

with st.expander("➕ Adicionar Venda"):
    with st.form("nova_venda", clear_on_submit=True):
        st.subheader("Dados da venda")
        col1, col2, col3 = st.columns(3)

        with col1:
            data = st.date_input("Data", value=pd.Timestamp.today().date())
            acao = st.text_input("Ação")
            status = st.selectbox(
                "Status",
                ["Contato", "Cliente em Potencial", "Cliente", "Parceiro"],
            )

        with col2:
            nome = st.text_input("Nome")
            sobrenome = st.text_input("Sobrenome")
            contato = st.text_input("Telefone")

        with col3:
            peca = st.text_input("Peça")
            estagio_da_peca = st.selectbox(
                "Estágio da peça",
                ["Não Iniciado", "Em progresso", "Concluído", "Perdido"],
            )
            valor_da_peca = st.number_input(
                "Valor da peça (R$)",
                min_value=0.0,
                step=0.01,
                format="%.2f",
            )

        st.divider()
        confirmar = st.form_submit_button("💾 Adicionar venda")

    if confirmar:
        receita_bruta_da_venda = valor_da_peca
        custos_da_venda = 0.0
        receita_liquida_da_venda = receita_bruta_da_venda - custos_da_venda

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
            "Receita Bruta": receita_bruta_da_venda,
            "Custos": custos_da_venda,
            "Receita Líquida": receita_liquida_da_venda,
        }

        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        salvar_dados(df)

        st.toast(f"Venda de {nome} adicionada com sucesso!")
        st.rerun()

st.dataframe(df, width="stretch")
