import pandas as pd
import numpy as np
# import plotly.express as px
# import re
# import folium
# from haversine import haversine

import streamlit as st
# from streamlit_folium import folium_static

st.set_page_config(page_title='Analise Geral', layout='wide', page_icon='🧩')

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

st.header('Relatório - Visão geral')

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
tb1, tb2, tb3 = st.tabs(['Sexo', 'Educação', 'Renda'])

with tb1:
    # Total por sexo
    sexo_data = data_all['Sex'].reset_index().groupby('Sex').count().reset_index()
    sexo_data.columns = ['Sexo', 'Quantidade']

    # Diabetico por sexo
    sexo_data_diabetico = data_all[data_all['Diabetes_binary'] == 1]
    sexo_data_diabetico = sexo_data_diabetico['Sex'].reset_index().groupby('Sex').count().reset_index()
    sexo_data_diabetico.columns = ['Sexo', 'Quantidade']

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            col1.metric('Total Masculino', sexo_data[sexo_data['Sexo'] == 'Masculino']['Quantidade'])
        with col2:
            col2.metric('Diabetico Masculino', sexo_data_diabetico[sexo_data['Sexo'] == 'Feminino']['Quantidade'])
        with col3:
            col3.metric('Total Feminino', sexo_data[sexo_data['Sexo'] == 'Feminino']['Quantidade'])
        with col4:
            col4.metric('Diabetico Feminino', sexo_data_diabetico[sexo_data['Sexo'] == 'Feminino']['Quantidade'])

    with st.container():
        st.header('Total por sexo filtrado')
        sexo_data_filter = data['Sex'].reset_index().groupby('Sex').count().reset_index()
        sexo_data_filter.columns = ['Sexo', 'Quantidade']
        st.table(sexo_data_filter)

    with st.container():
        st.header('Diabeticos por sexo filtrado')
        sexo_data_diabetico_filter = data[data['Diabetes_binary'] == 1]
        sexo_data_diabetico_filter = sexo_data_diabetico_filter['Sex'].reset_index().groupby('Sex').count().reset_index()
        sexo_data_diabetico_filter.columns = ['Sexo', 'Quantidade']
        st.table(sexo_data_diabetico_filter)

with tb2:
    # Total por educacao
    educacao_data = data_all['Education'].reset_index().groupby('Education').count().reset_index()
    educacao_data.columns = ['Educacao', 'Quantidade']

    # Diabetico por educacao
    educacao_data_diabetico = data_all[data_all['Diabetes_binary'] == 1]
    educacao_data_diabetico = educacao_data_diabetico['Education'].reset_index().groupby('Education').count().reset_index()
    educacao_data_diabetico.columns = ['Educacao', 'Quantidade']

    with st.container():
        st.header('Total diabeticos')
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            col1.metric('Nunca Frequentou', educacao_data_diabetico[educacao_data['Educacao'] == 'Nunca frequentou']['Quantidade'])
        with col2:
            col2.metric('Ensino Fundamental', educacao_data_diabetico[educacao_data['Educacao'] == 'Ensino Fundamental']['Quantidade'])
        with col3:
            col3.metric('Ens. Médio Incompleto', educacao_data[educacao_data['Educacao'] == 'Ensino médio incompleto']['Quantidade'])
        with col4:
            col4.metric('Concluiu Ensino Médio', educacao_data[educacao_data['Educacao'] == 'Concluiu o ensino médio']['Quantidade'])
        with col5:
            col5.metric('Escola Técnica', educacao_data_diabetico[educacao_data['Educacao'] == 'Alguma faculdade ou escola técnica']['Quantidade'])
        with col6:
            col6.metric('Graduado na faculdade', educacao_data_diabetico[educacao_data['Educacao'] == 'Graduado na faculdade']['Quantidade'])

    with st.container():
        educacao_data_diabetico_filter = data[data['Diabetes_binary'] == 1]
        educacao_data_diabetico_filter = educacao_data_diabetico_filter['Education'].reset_index().groupby('Education').count().reset_index()
        educacao_data_diabetico_filter.columns = ['Educacao', 'Diabetico']

        st.header('Total por educacao filtrado')
        educacao_data_filter = data['Education'].reset_index().groupby('Education').count().reset_index()
        educacao_data_filter.columns = ['Educacao', 'Quantidade']
        educacao_data_diabetico_filter['Quantidade'] = educacao_data_filter['Quantidade']
        st.table(educacao_data_diabetico_filter)


with tb3:
    # Total por educacao
    renda_data = data_all['Income'].reset_index().groupby('Income').count().reset_index()
    renda_data.columns = ['Renda', 'Quantidade']

    # Diabetico por educacao
    renda_data_diabetico = data_all[data_all['Diabetes_binary'] == 1]
    renda_data_diabetico = renda_data_diabetico['Income'].reset_index().groupby('Income').count().reset_index()
    renda_data_diabetico.columns = ['Renda', 'Quantidade']

    with st.container():
        st.header('Total diabeticos')
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        with col1:
            col1.metric('Até 10Mil', renda_data_diabetico[renda_data['Renda'] == 'Até 10Mil']['Quantidade'])
        with col2:
            col2.metric('10Mil - 15Mil', renda_data_diabetico[renda_data['Renda'] == '10Mil - 15Mil']['Quantidade'])
        with col3:
            col3.metric('15Mil - 20Mil', renda_data[renda_data['Renda'] == '15Mil - 20Mil']['Quantidade'])
        with col4:
            col4.metric('20Mil - 25Mil', renda_data[renda_data['Renda'] == '20Mil - 25Mil']['Quantidade'])
        with col5:
            col5.metric('25Mil - 35Mil', renda_data_diabetico[renda_data['Renda'] == '25Mil - 35Mil']['Quantidade'])
        with col6:
            col6.metric('35Mil - 50Mil', renda_data_diabetico[renda_data['Renda'] == '35Mil - 50Mil']['Quantidade'])
        with col7:
            col7.metric('50Mil - 75Mil', renda_data_diabetico[renda_data['Renda'] == '50Mil - 75Mil']['Quantidade'])
        with col8:
            col8.metric('Mais 75Mil', renda_data_diabetico[renda_data['Renda'] == 'Mais 75Mil']['Quantidade'])

    with st.container():
        renda_data_diabetico_filter = data[data['Diabetes_binary'] == 1]
        renda_data_diabetico_filter = renda_data_diabetico_filter['Income'].reset_index().groupby('Income').count().reset_index()
        renda_data_diabetico_filter.columns = ['Renda', 'Diabetico']

        st.header('Total por renda por anor filtrado')
        renda_data_filter = data['Income'].reset_index().groupby('Income').count().reset_index()
        renda_data_filter.columns = ['Renda', 'Quantidade']
        renda_data_diabetico_filter['Quantidade'] = renda_data_filter['Quantidade']
        st.table(renda_data_diabetico_filter)
