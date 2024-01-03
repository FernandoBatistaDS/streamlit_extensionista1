import pandas as pd
import numpy as np
# import plotly.express as px
# import re
# import folium
# from haversine import haversine

import streamlit as st
# from streamlit_folium import folium_static

st.set_page_config(page_title='Análise das Variaveis', layout='wide', page_icon='🧪')

# -------------------
# FUNÇÕES
# -------------------

# ----------------------------------------- Start Logíca ----------------------------------------- #
# ---------------------
# Import dataset
# ---------------------
data        =   pd.read_csv('datasets/diabetes_binary_health_indicators_BRFSS2015.csv')
data        =   data.astype(int)

# ################## VISÃO Negocio ################## #

# ------------> BARRA LATERAL SIDEBAR

# ------------> BARRA LATERAL SIDEBAR
dt_min = data['Age'].min()
dt_max = data['Age'].max()

st.header('Relatório - Análise das Variaveis')

# --------------
# STREAMLIT - Filtrar por idade
# --------------
age_slider = st.sidebar.slider(
    'Qual idade?',
    value=dt_max,
    min_value=dt_min,
    max_value=dt_max
)

# --------------
# STREAMLIT - Filtrar por sexo
# --------------
data['Sex'] = data['Sex'].map({0: 'Feminino', 1: 'Masculino'})
sex_option = st.sidebar.multiselect('Selecionar sexo!', data['Sex'].unique(), default=data['Sex'].unique())


# --------------
# STREAMLIT - Níveis educacionais
# --------------
data['Education'] = data['Education'].map({
    1: 'Nunca frequentou',
    2: 'Ensino Fundamental',
    3: 'Ensino médio incompleto',
    4: 'Concluiu o ensino médio',
    5: 'Alguma faculdade ou escola técnica',
    6: 'Graduado na faculdade',
})

education_option = st.sidebar.multiselect('Níveis educacionais?', data['Education'].unique(), default=data['Education'].unique())


# --------------
# STREAMLIT - Escala de renda anual
# --------------
data['Income'] = data['Income'].map({
    1:  'Até 10Mil',
    2:  '10Mil - 15Mil',
    3:  '15Mil - 20Mil',
    4:  '20Mil - 25Mil',
    5:  '25Mil - 35Mil',
    6:  '35Mil - 50Mil',
    7:  '50Mil - 75Mil',
    8:  'Mais 75Mil'
})

income_option = st.sidebar.multiselect('Níveis educacionais?', data['Income'].unique(), default=data['Income'].unique())



st.sidebar.markdown("""---""")
st.sidebar.markdown("### Powered by Fernando Batista")
st.sidebar.markdown("##### RU: 4530686")
st.sidebar.markdown("##### Uninter")


# --------------
# STREAMLIT - Filtro de datas
# --------------

# Copy do dataframe original
data_all    =   data.copy()

# Filtro de age
linhas_selecionadas = data['Age'] <= age_slider
data = data.loc[linhas_selecionadas, :]

# Filtro de Sex
linhas_selecionadas = data['Sex'].isin(sex_option)
data = data.loc[linhas_selecionadas, :]

# Filtro de Education
linhas_selecionadas = data['Education'].isin(education_option)
data = data.loc[linhas_selecionadas, :]

# Filtro de Income
linhas_selecionadas = data['Income'].isin(income_option)
data = data.loc[linhas_selecionadas, :]

# --------------
# STREAMLIT - LAYOUT CONTAINER
# --------------
tb1, tb2 = st.tabs(['Atividade física', 'Saúde'])

with tb1:
    with st.container():
        st.markdown(
                """
                    ### Dificuldade para andar ou subir escadas?
                    Quem tem mais dificudades, provavelmente tem diabates, vamos ver os dados!
                """
        )

        df_walk = data.loc[:, ['DiffWalk', 'Age', 'Diabetes_binary']];
        df_walk = df_walk.loc[:, ['DiffWalk', 'Age', 'Diabetes_binary']].reset_index().groupby(['DiffWalk', 'Diabetes_binary']).sum().reset_index()
        df_walk


with tb2:
    with st.container():
        st.markdown(
                """
                    ### Dificuldade para andar ou subir escadas?
                    Quem tem mais dificudades, provavelmente tem diabates, vamos ver os dados!
                """
        )

