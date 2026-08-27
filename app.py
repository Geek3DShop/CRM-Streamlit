import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from services.auth import login, is_authenticated, logout
from pages.login import login

load_dotenv()
clientes_path = os.getenv("CLIENTES_PATH")
custos_path = os.getenv("CUSTOS_PATH")

st.set_page_config(
    page_title="CRM Geek 3D Shop",
    page_icon="💰",
    layout="wide"
)
if not is_authenticated():
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    login()
    st.stop()

def formatar_reais(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

def salvar_dados(df):
    df.to_excel(clientes_path, index=False)

clientes = pd.read_excel(clientes_path)

try:
    custos = pd.read_excel(custos_path)
    total_custos = custos["Custos"].sum()
except FileNotFoundError:
    total_custos = 0.0

receita_bruta = clientes["Valor da peça"].sum()
receita_liquida = receita_bruta - total_custos

col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
col1.title("CRM Geek 3D Shop")
col2.metric(
    "💵 Receita Bruta",
    formatar_reais(receita_bruta)
)
col3.metric(
    "💸 Custos",
    formatar_reais(total_custos)
)
col4.metric(
    "💰 Receita Líquida",
    formatar_reais(receita_liquida)
)
col5.metric(
    "📈 Número de vendas",
    len(clientes)
)
st.caption("Controle de clientes, vendas, custos e lucro")

with st.sidebar:
    st.write("### 👤 Usuário autenticado")
    if st.button("🚪 Sair", use_container_width=True):
        logout()
if "form_version" not in st.session_state:
    st.session_state.form_version = 0

form_version = st.session_state.form_version

with st.expander("➕ Adicionar Venda"):
    with st.form("nova_venda"):
        st.subheader("Dados da venda")
        col1, col2, col3 = st.columns(3)
        with col1:
            data = st.date_input(
                "Data",
                value=pd.Timestamp.today().date(),
                key=f"venda_data_{form_version}"
            )
            nome = st.text_input(
                "Nome",
                key=f"venda_nome_{form_version}"
            )
            sobrenome = st.text_input(
                "Sobrenome",
                key=f"venda_sobrenome_{form_version}"
            )
        with col2:
            status = st.selectbox(
                "Status",
                [
                    "Contato",
                    "Cliente em Potencial",
                    "Cliente",
                    "Parceiro"
                ],
                key=f"venda_status_{form_version}"
            )
            contato = st.text_input(
                "Contato",
                key=f"venda_contato_{form_version}"
            )
            peca = st.text_input(
                "Peça",
                key=f"venda_peca_{form_version}"
            )
        with col3:
            estagio_da_peca = st.selectbox(
                "Estágio da peça",
                [
                    "Não Iniciado",
                    "Em progresso",
                    "Concluído",
                    "Perdido"
                ],
                key=f"venda_estagio_{form_version}"
            )
            acao = st.text_input(
                "Ação",
                key=f"venda_acao_{form_version}"
            )
            valor_da_peca = st.number_input(
                "Valor da peça (R$)",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key=f"venda_valor_{form_version}"
            )
        st.divider()
        confirmar = st.form_submit_button(
            "💾 Adicionar venda"
        )
if confirmar:
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
    clientes = pd.concat(
        [
            clientes,
            pd.DataFrame([nova_linha])
        ],
        ignore_index=True
    )
    salvar_dados(clientes)
    st.session_state.form_version += 1
    st.success(
        f"Venda de {nome} adicionada com sucesso!"
    )
    st.rerun()

st.dataframe(
    clientes,
    width="stretch"
)