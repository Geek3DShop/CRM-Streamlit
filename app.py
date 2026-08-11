# import os
# import streamlit as st
# import pandas as pd
# from dotenv import load_dotenv

# load_dotenv()

# st.set_page_config(page_title="CRM Geek 3D Shop", layout="wide")

# st.title("CRM Geek 3D Shop")

# path = os.getenv("CRM_PATH")
# df = pd.read_excel(path)
# df = df.dropna(axis=1, how="all")

# st.dataframe(df, width="stretch")


import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
path = os.getenv("CRM_PATH")

st.set_page_config(page_title="CRM Geek 3D Shop",  page_icon="💰", layout="wide")

st.title("CRM Geek 3D Shop")
st.caption("Controle de clientes, vendas, custos e lucro")

def carrega_dados():
    if(path):
        df = pd.read_excel(path)
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
    df.to_excel(path, index=False)

df = carrega_dados()
   
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
                                                         #     Receita_Bruta	 =  st.number_input("Receita_Bruta", min_value=0.0, step=0.01) 
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
        #     Custos	 = st.number_input("Custos", min_value=0.0, step=0.01)

        #     Receita_Líquida = st.number_input("Receita_Líquida", min_value=0.0, step=0.01)

        #     confirmar = st.form_submit_button("Adicionar venda")

        # if confirmar:

        #     df = pd.read_excel(path)
        #     nova_linha = { "Data": Data, "Ação": Ação, "Status": Status, 
        #                 "Nome": Nome, "Sobrenome": Sobrenome, 
        #                 "Contato": Contato, "Peça": Peça, 
        #                 "Estágio_da_peça": Estágio_da_peça, 
        #                 "Valor_da_peça": Valor_da_peça, 
        #                 "Receita_Bruta": Receita_Bruta, 
        #                 "Custos": Custos, "Receita_Líquida": Receita_Líquida }
        #     df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)

        #     st.success("Venda adicionada com sucesso!")