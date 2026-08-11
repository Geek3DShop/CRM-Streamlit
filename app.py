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

st.set_page_config(page_title="CRM Geek 3D Shop", layout="wide")

st.title("CRM Geek 3D Shop")
df = pd.read_excel(path)
st.dataframe(df, width="stretch")
with st.expander("Adicionar Venda"):
    with st.form("nova_venda"):
        Data = st.date_input("Data")

        Ação = st.text_input("Ação")

        Status	= st.selectbox( "Status", [ "Cliente", "Contato", "Parceiro", "Cliente em Potencial" ] )
        Nome = st.text_input("Nome")	

        Sobrenome	= st.text_input("Sobrenome")

        Contato	= st.number_input("telefone")

        Peça	= st.text_input("Peça")

        Estágio_da_peça	 = st.selectbox( "Estágio da peça", [ "Não Iniciado", "Em progresso", "Concluído", "Perdido" ] )

        Valor_da_peça = st.number_input("Valor", min_value=0.0, step=0.01)

        Receita_Bruta	 =  st.number_input("Receita_Bruta", min_value=0.0, step=0.01) 

        Custos	 = st.number_input("Custos", min_value=0.0, step=0.01)

        Receita_Líquida = st.number_input("Receita_Líquida", min_value=0.0, step=0.01)

        confirmar = st.form_submit_button("Adicionar venda")

    if confirmar:

        df = pd.read_excel(path)
        nova_linha = { "Data": Data, "Ação": Ação, "Status": Status, 
                    "Nome": Nome, "Sobrenome": Sobrenome, 
                    "Contato": Contato, "Peça": Peça, 
                    "Estágio_da_peça": Estágio_da_peça, 
                    "Valor_da_peça": Valor_da_peça, 
                    "Receita_Bruta": Receita_Bruta, 
                    "Custos": Custos, "Receita_Líquida": Receita_Líquida }
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        df.to_excel(path, index=False)
        st.success("Venda adicionada com sucesso!")

