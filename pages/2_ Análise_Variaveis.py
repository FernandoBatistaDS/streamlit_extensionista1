import pandas               as  pd
import numpy                as  np
import matplotlib.pyplot    as  plt
import streamlit            as  st
import seaborn              as sns


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
    st.markdown(
            """
                <h2 style='text-align: center;'>Idades com dificuldades para andar ou subir escadas</h2>
                <p style='text-align: center;'>Quem tem mais dificudades, provavelmente tem diabates, vamos ver os dados!</p>
            """,
            unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <h3 style='text-align: center;'>Diabéticos</h3>
            """,
            unsafe_allow_html=True
        )

        df_walk                         =   data.loc[:, ['Age', 'DiffWalk', 'Diabetes_binary']]
        df_walk                         =   df_walk.loc[:, ['Age', 'DiffWalk', 'Diabetes_binary']].groupby(['Age', 'DiffWalk']).sum().reset_index()
        df_walk.columns                 =   ['Idade', 'Dificuldade Andar', 'Quantidade']

        # Separação no eixo "X"
        species                         =   list(df_walk['Idade'].unique())
        # species

        andar_counts = {
            'Tem dificuldade': np.array(df_walk.loc[df_walk['Dificuldade Andar'] == 1, 'Quantidade']),
            'Não tem dificuldade': np.array(df_walk.loc[df_walk['Dificuldade Andar'] == 0, 'Quantidade']),
        }

        width = 0.8  # the width of the bars: can also be len(x) sequence

        fig, ax = plt.subplots()
        bottom  = np.zeros(len(species))

        for andar, andar_count in andar_counts.items():
            p = ax.bar(species, andar_count, width, label=andar, bottom=bottom)
            bottom += andar_count

        ax.set_title('Idade dos diabéticos')
        ax.legend()

        st.pyplot(plt)

    with col2:
        st.markdown(
            """
            <h3 style='text-align: center;'>Não diabéticos</h3>
            """,
            unsafe_allow_html=True
        )

        df_walk                         =   data.loc[data['Diabetes_binary'] == 0, ['Age', 'DiffWalk', 'Diabetes_binary']]
        df_walk                         =   df_walk.loc[:, ['Age', 'DiffWalk', 'Diabetes_binary']].groupby(['Age', 'DiffWalk']).count().reset_index()
        df_walk.columns                 =   ['Idade', 'Dificuldade Andar', 'Quantidade']

        # Separação no eixo "X"
        species                         =   list(df_walk['Idade'].unique())
        # species

        andar_counts = {
            'Tem dificuldade': np.array(df_walk.loc[df_walk['Dificuldade Andar'] == 1, 'Quantidade']),
            'Não tem dificuldade': np.array(df_walk.loc[df_walk['Dificuldade Andar'] == 0, 'Quantidade']),
        }

        width = 0.8  # the width of the bars: can also be len(x) sequence

        fig, ax = plt.subplots()
        bottom  = np.zeros(len(species))

        for andar, andar_count in andar_counts.items():
            p = ax.bar(species, andar_count, width, label=andar, bottom=bottom)
            bottom += andar_count

        ax.set_title('Idade dos não diabéticos')
        ax.legend()

        st.pyplot(plt)


with tb2:
    st.markdown(
            """
                <h2 style='text-align: center;'>Saúde</h2>
            """,
            unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <h3 style='text-align: center;'>Plano de saúde</h3>
            """,
            unsafe_allow_html=True
        )

        df_plan                     =   data.loc[:, ['AnyHealthcare', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'AnyHealthcare']).count().reset_index()
        df_plan.columns             =   ['Diabetico', 'Plano de Saúde', 'Quantidade']
        df_plan['Diabetico']        =   df_plan['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_plan['Plano de Saúde']   =   df_plan['Plano de Saúde'].map({ 0: 'Não tem', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Plano de Saúde', y='Quantidade', hue='Diabetico', data=df_plan)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Tem plano de saúde?')
        plt.ylabel('Quantidades')
        plt.title('Plano de saúde')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

    with col2:
        st.markdown(
            """
            <h3 style='text-align: center;'>Não consultou um médico por ser caro?</h3>
            """,
            unsafe_allow_html=True
        )

        df_cost                     =   data.loc[:, ['NoDocbcCost', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'NoDocbcCost']).count().reset_index()
        df_cost.columns             =   ['Diabetico', 'Consulta', 'Quantidade']
        df_cost['Diabetico']        =   df_cost['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_cost['Consulta']         =   df_cost['Consulta'].map({ 0: 'Pôde consultar', 1: 'Não pôde consultar'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Consulta', y='Quantidade', hue='Diabetico', data=df_cost)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Consulta')
        plt.ylabel('Quantidades')
        plt.title('Consultas por ser caro')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

with st.container():
    st.markdown(
            """
                <h2 style='text-align: center;'>Como o paciente se sente de saúde: escala de 1 a 5</h2>
                <div style='text-align: center;'>
                    1 = Excelente<br>
                    2 = Muito boa<br>
                    3 = Boa<br>
                    4 = Razoável<br>
                    5 = Ruim
                <div>
                <br>
            """,
            unsafe_allow_html=True
    )

    df_plan                     =   data.loc[:, ['GenHlth', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'GenHlth']).count().reset_index()
    df_plan.columns             =   ['Diabetico', 'Saúde', 'Quantidade']
    df_plan['Diabetico']        =   df_plan['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
    df_plan['Saúde']   =   df_plan['Saúde'].map({ 1: '1 - Excelente', 2: '2 - Muito boa', 3: '3 - Boa', 4: '4 - Razoável', 5: '5 - Ruim'})

    # Criando o gráfico de barras com hue
    plt.figure(figsize=(8, 6))
    sns.lineplot(x='Saúde', y='Quantidade', hue='Diabetico', data=df_plan)

    # Adicionando rótulos ao eixo x e y
    plt.xlabel('Nota para a saúde')
    plt.ylabel('Quantidades')
    plt.title('Saúde')

    # # Exibindo a legenda
    # plt.legend(title='Jeu')

    # Exibindo o gráfico
    st.pyplot(plt)
