from PIL import Image
import streamlit as st

st.set_page_config(
    page_title='Inicio do projeto',
    layout='wide',
    page_icon='👨‍⚕️'
)

st.sidebar.markdown("# ")
st.sidebar.markdown("## ATIVIDADES EXTENSIONISTAS I")
st.sidebar.markdown("""---""")

st.write("# Análise de dados")
st.markdown(
    """
        #### Diabéticos e não diabéticos

        Dados retirados do site:
            https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
        ### Como ultilizar esses Dashbord?
        - Visão Geral:
            - O Filtro de idade são com as seguintes classificações
                -   Categoria 1: 18-24 anos
                -   Categoria 2: 25-29 anos
                -   Categoria 3: 30-34 anos
                -   Categoria 4: 35-39 anos
                -   Categoria 5: 40-44 anos
                -   Categoria 6: 45-49 anos
                -   Categoria 7: 50-54 anos
                -   Categoria 8: 55-59 anos
                -   Categoria 9: 60-64 anos
                -   Categoria 10: 65-69 anos
                -   Categoria 11: 70-74 anos
                -   Categoria 12: 75-79 anos
                -   Categoria 13: 80 anos ou mais
            - Visão Tática: Indicadores semanais de crescimento
            - Visão Geográfica: Insights de geolocalizão.
        - Visão Entregador:
            - Acompanhamento dos indicadores semanais de crescimento
        - Visão Restaurante:
            - Indicadores semanais de crescimento dos restaurantes
    """
)