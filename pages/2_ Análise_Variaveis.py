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
tb1, tb2, tb3, tb4 = st.tabs(['Atividade física', 'Saúde', 'Alimentação', 'Doença'])

with tb1:
    st.markdown(
            """
                <h2 style='text-align: center;'>Idades com dificuldades para andar ou subir escadas</h2>
                <p style='text-align: center;'>Quem tem mais dificudades, provavelmente tem diabates, vamos ver os dados!</p>
            """,
            unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <h4 style='text-align: center;'>Diabéticos</h4>
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
            <h4 style='text-align: center;'>Atividade nos últimos 30 dias</h4>
            """,
            unsafe_allow_html=True
        )

        df_cost                     =   data.loc[:, ['PhysActivity', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'PhysActivity']).count().reset_index()
        df_cost.columns             =   ['Diabetico', 'Consulta', 'Quantidade']
        df_cost['Diabetico']        =   df_cost['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_cost['Consulta']         =   df_cost['Consulta'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Consulta', y='Quantidade', hue='Diabetico', data=df_cost)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Fez atividade física nos últimos 30 dias?')
        plt.ylabel('Quantidades')
        plt.title('Atividade fisica')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

    with col3:
        st.markdown(
            """
            <h4 style='text-align: center;'>Não diabéticos</h4>
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
            <h4 style='text-align: center;'>Plano de saúde</h4>
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
            <h4 style='text-align: center;'>Não consultou um médico por ser caro?</h4>
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

    with st.container():
        st.markdown(
                """
                    <h2 style='text-align: center;'>Saúde mental</h2>
                """,
                unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <h4 style='text-align: center;'>Saúde mental</h4>
                Por quantos dias durante os últimos 30 dias sua saúde mental não foi boa?
                """,
                unsafe_allow_html=True
            )

            df_ment                     =   data.loc[:, ['MentHlth', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'MentHlth']).count().reset_index()
            df_ment.columns             =   ['Diabetico', 'Dias saúde mental', 'Quantidade']
            df_ment['Diabetico']        =   df_ment['Diabetico'].map({ 0: 'Não', 1: 'Sim'})

            # Criando o gráfico de barras com hue
            plt.figure(figsize=(8, 6))
            sns.lineplot(x='Dias saúde mental', y='Quantidade', hue='Diabetico', data=df_ment)

            # Adicionando rótulos ao eixo x e y
            plt.xlabel('Quantidades de dias ruins de saúde mental nos ultimos 30 dias')
            plt.ylabel('Quantidades')
            plt.title('Número de dias com saúde mental comprometida nos últimos 30 dias')

            # # Exibindo a legenda
            # plt.legend(title='Jeu')

            # Exibindo o gráfico
            st.pyplot(plt)
            df_ment_table = df_ment[['Diabetico', 'Dias saúde mental', 'Quantidade']].sort_values('Dias saúde mental').reset_index(drop=True)
            st.table(df_ment_table)

        with col2:
            st.markdown(
                """
                <h4 style='text-align: center;'>Saúde física</h4>
                Por quantos dias durante os últimos 30 dias sua saúde física não foi boa?
                """,
                unsafe_allow_html=True
            )

            df_phys                     =   data.loc[:, ['PhysHlth', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'PhysHlth']).count().reset_index()
            df_phys.columns             =   ['Diabetico', 'Dias saúde física', 'Quantidade']
            df_phys['Diabetico']        =   df_phys['Diabetico'].map({ 0: 'Não', 1: 'Sim'})

            # Criando o gráfico de barras com hue
            plt.figure(figsize=(8, 6))
            sns.lineplot(x='Dias saúde física', y='Quantidade', hue='Diabetico', data=df_phys)

            # Adicionando rótulos ao eixo x e y
            plt.xlabel('Quantidades de dias ruins de saúde física nos ultimos 30 dias')
            plt.ylabel('Quantidades')
            plt.title('Número de dias com saúde física comprometida nos últimos 30 dias')

            # # Exibindo a legenda
            # plt.legend(title='Jeu')

            # Exibindo o gráfico
            st.pyplot(plt)
            df_phys_table = df_phys[['Diabetico', 'Dias saúde física', 'Quantidade']].sort_values('Dias saúde física').reset_index(drop=True)
            st.table(df_phys_table)

with tb3:
    st.markdown(
            """
                <h2 style='text-align: center;'>Alimentação</h2>
            """,
            unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <h4 style='text-align: center;'>Frutas</h4>
            """,
            unsafe_allow_html=True
        )

        df_fruits                   =   data.loc[:, ['Fruits', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'Fruits']).count().reset_index()
        df_fruits.columns           =   ['Diabetico', 'Frutas', 'Quantidade']
        df_fruits['Diabetico']      =   df_fruits['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_fruits['Frutas']         =   df_fruits['Frutas'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Frutas', y='Quantidade', hue='Diabetico', data=df_fruits)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Consumir frutas 1 ou mais vezes ao dia?')
        plt.ylabel('Quantidades')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

    with col2:
        st.markdown(
            """
            <h4 style='text-align: center;'>Vegetais</h4>
            """,
            unsafe_allow_html=True
        )

        df_veggies                     =   data.loc[:, ['Veggies', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'Veggies']).count().reset_index()
        df_veggies.columns             =   ['Diabetico', 'Vegetais', 'Quantidade']
        df_veggies['Diabetico']        =   df_veggies['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_veggies['Vegetais']         =   df_veggies['Vegetais'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Vegetais', y='Quantidade', hue='Diabetico', data=df_veggies)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Consumir Legumes 1 ou mais vezes ao dia?')
        plt.ylabel('Quantidades')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

with tb4:
    st.markdown(
            """
                <h2 style='text-align: center;'>Doenças</h2>
            """,
            unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <h4 style='text-align: center;'>Pressão arterial alta</h4>
            <br>
            """,
            unsafe_allow_html=True
        )

        df_pb                   =   data.loc[:, ['HighBP', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'HighBP']).count().reset_index()
        df_pb.columns           =   ['Diabetico', 'Pressão alta', 'Quantidade']
        df_pb['Diabetico']      =   df_pb['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_pb['Pressão alta']   =   df_pb['Pressão alta'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Pressão alta', y='Quantidade', hue='Diabetico', data=df_pb)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Pressão alta?')
        plt.ylabel('Quantidades')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

    with col2:
        st.markdown(
            """
            <h4 style='text-align: center;'>Doença coronariana ou infarto do miocárdio</h4>
            """,
            unsafe_allow_html=True
        )

        df_chol                     =   data.loc[:, ['HeartDiseaseorAttack', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'HeartDiseaseorAttack']).count().reset_index()
        df_chol.columns             =   ['Diabetico', 'Teve doença', 'Quantidade']
        df_chol['Diabetico']        =   df_chol['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_chol['Teve doença']      =   df_chol['Teve doença'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Teve doença', y='Quantidade', hue='Diabetico', data=df_chol)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Teve alguma dessa?')
        plt.ylabel('Quantidades')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

    with col3:
        st.markdown(
            """
            <h4 style='text-align: center;'>Colesterol alto</h4>
            <br>
            """,
            unsafe_allow_html=True
        )

        df_chol                     =   data.loc[:, ['HighChol', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'HighChol']).count().reset_index()
        df_chol.columns             =   ['Diabetico', 'Colesterol alto', 'Quantidade']
        df_chol['Diabetico']        =   df_chol['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_chol['Colesterol alto']         =   df_chol['Colesterol alto'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Colesterol alto', y='Quantidade', hue='Diabetico', data=df_chol)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Colesterol alto?')
        plt.ylabel('Quantidades')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <h4 style='text-align: center;'>Verificação de colesterol em 5 anos</h4>
            """,
            unsafe_allow_html=True
        )

        df_chol                     =   data.loc[:, ['CholCheck', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'CholCheck']).count().reset_index()
        df_chol.columns             =   ['Diabetico', 'Colesterol alto', 'Quantidade']
        df_chol['Diabetico']        =   df_chol['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_chol['Colesterol alto']         =   df_chol['Colesterol alto'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Colesterol alto', y='Quantidade', hue='Diabetico', data=df_chol)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Colesterol alto nos ultimos 5 anos?')
        plt.ylabel('Quantidades')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

    with col2:
        st.markdown(
            """
            <h4 style='text-align: center;'>Índice de massa corporal</h4>
            """,
            unsafe_allow_html=True
        )

        df_chol                     =   data.loc[:, ['BMI', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'BMI']).count().reset_index()
        df_chol.columns             =   ['Diabetico', 'IMC', 'Quantidade']
        df_chol['Diabetico']        =   df_chol['Diabetico'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.lineplot(x='IMC', y='Quantidade', hue='Diabetico', data=df_chol)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('IMC')
        plt.ylabel('Quantidades')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <h4 style='text-align: center;'>Fumou + de 100 cigarros em toda a vida</h4>
            """,
            unsafe_allow_html=True
        )

        df_chol                     =   data.loc[:, ['Smoker', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'Smoker']).count().reset_index()
        df_chol.columns             =   ['Diabetico', 'Smoker', 'Quantidade']
        df_chol['Diabetico']        =   df_chol['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_chol['Smoker']           =   df_chol['Smoker'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Smoker', y='Quantidade', hue='Diabetico', data=df_chol)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Fumou + de 100 cigarros?')
        plt.ylabel('Quantidades')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)

    with col2:
        st.markdown(
            """
            <h4 style='text-align: center;'>Teve um derrame</h4>
            """,
            unsafe_allow_html=True
        )

        df_chol                     =   data.loc[:, ['Stroke', 'Diabetes_binary']].reset_index().groupby(['Diabetes_binary', 'Stroke']).count().reset_index()
        df_chol.columns             =   ['Diabetico', 'Stroke', 'Quantidade']
        df_chol['Diabetico']        =   df_chol['Diabetico'].map({ 0: 'Não', 1: 'Sim'})
        df_chol['Stroke']           =   df_chol['Stroke'].map({ 0: 'Não', 1: 'Sim'})

        # Criando o gráfico de barras com hue
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Stroke', y='Quantidade', hue='Diabetico', data=df_chol)

        # Adicionando rótulos ao eixo x e y
        plt.xlabel('Já teve um derrame?')
        plt.ylabel('Quantidades')

        # # Exibindo a legenda
        # plt.legend(title='Jeu')

        # Exibindo o gráfico
        st.pyplot(plt)
