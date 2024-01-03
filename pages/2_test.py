################## Paginas 
"""
    # https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators

    """

import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so

df_3classe    =   pd.read_csv('datasets/diabetes_012_health_indicators_BRFSS2015.csv')
df_2classe    =   pd.read_csv('datasets/diabetes_binary_health_indicators_BRFSS2015.csv')
df_5050       =   pd.read_csv('datasets/diabetes_binary_5050split_health_indicators_BRFSS2015.csv')

df = df_2classe.astype(int)

df.columns

df.loc[:, ['Smoker', 'Diabetes_binary']].groupby('Smoker').count()

"""## Graficos de fumantes e não fumantes"""

# Graficos para os fumantes, seleciona as colunas certas
df_fumante_ou_nao = df.loc[:, ['Diabetes_binary', 'Sex', 'Smoker']];
df_fumante_ou_nao.columns = ['Diabéticos', 'Sexo', 'Fumante'];

# Coloca valores certos para Sexo e Diabéticos
df_fumante_ou_nao['Sexo'] = df_fumante_ou_nao['Sexo'].map({1: 'Masculino', 0: 'Feminino'});
df_fumante_ou_nao['Diabéticos'] = df_fumante_ou_nao['Diabéticos'].map({1: 'Sim', 0: 'Não'});

# Faz groupby para saber quantos Diabeticos fumentes e não fumantes existem
df_fumante_ou_nao = df_fumante_ou_nao.reset_index().groupby(['Diabéticos', 'Sexo', 'Fumante']).count().reset_index()
df_fumante_ou_nao.columns = ['Diabéticos', 'Sexo', 'Fumante_Binario', 'Fumante']

df_fumante_ou_nao

# Total fumantes e não fumantes
total_fumantes_e_naoFumantes = df_fumante_ou_nao.loc[:, ['Fumante_Binario', 'Fumante']].groupby(['Fumante_Binario']).sum().reset_index()
total_fumantes_e_naoFumantes['Fumante_Binario'] = df_fumante_ou_nao['Fumante_Binario'].map({1: 'Sim', 0: 'Não'});
total_fumantes_e_naoFumantes

# Total feminino e masculino
total_feminino_masculino = df_fumante_ou_nao.loc[:, ['Sexo', 'Fumante']].groupby(['Sexo']).sum().reset_index()
total_feminino_masculino

df_fumante = df_fumante_ou_nao[df_fumante_ou_nao['Fumante_Binario'] == 1]
# df_fumante
sns.barplot(df_fumante, x="Diabéticos", y="Fumante", hue="Sexo");

# Graficos para os fumantes
df_fumante = df_fumante_ou_nao[df_fumante_ou_nao['Fumante_Binario'] == 0]
sns.barplot(df_fumante, x="Diabéticos", y="Fumante", hue="Sexo");

# Graficos não fumantes
df_fumante = df.loc[:, ['Diabetes_binary', 'Sex', 'Smoker']];
df_fumante.columns = ['Diabéticos', 'Sexo', 'Fumante'];

df_fumante['Sexo'] = df_fumante['Sexo'].map({1: 'Masculino', 0: 'Feminino'});
df_fumante['Diabéticos'] = df_fumante['Diabéticos'].map({1: 'Sim', 0: 'Não'});

df_fumante = df_fumante[df_fumante['Fumante'] == 0]
df_fumante = df_fumante.groupby(['Sexo', 'Diabéticos']).count().reset_index()

sns.barplot(df_fumante, x="Diabéticos", y="Fumante", hue="Sexo");

"""## Graficos de 'HipertensaoAlta' e 'ColesterolAlto'"""

# Graficos para os 'HipertensaoAlta', 'ColesterolAlto'
df_high = df.loc[:, ['Sex', 'HighBP', 'HighChol', 'Diabetes_binary', 'CholCheck']];
df_high.columns = ['Sexo', 'HipertensaoAlta', 'ColesterolAlto', 'Diabéticos', '5AnosColesterol'];

# Coloca valores certos para HipertensaoAlta
df_high['HipertensaoAlta'] = df_high['HipertensaoAlta'].map({1: 'Sim', 0: 'Não'});

# Coloca valores certos para Verificar Colesterol
df_high['5AnosColesterol'] = df_high['5AnosColesterol'].map({1: 'Sim', 0: 'Não'});

# Coloca valores certos para ColesterolAlto
df_high['ColesterolAlto'] = df_high['ColesterolAlto'].map({1: 'Sim', 0: 'Não'});

# Coloca valores certos para Diabéticos
df_high['Diabéticos'] = df_high['Diabéticos'].map({1: 'Sim', 0: 'Não'});

# Coloca valores certos para Sexo e Diabéticos
df_high['Sexo'] = df_high['Sexo'].map({1: 'Masculino', 0: 'Feminino'});

df_high

# Faz groupby
df_high = df_high.reset_index().groupby(['Sexo', 'HipertensaoAlta', 'Diabéticos', 'ColesterolAlto', '5AnosColesterol']).count().reset_index()
df_high.columns = ['Sexo', 'HipertensaoAlta', 'Diabéticos', 'ColesterolAlto', '5AnosColesterol', 'Quantidade']
df_high

# HipertensaoAlta
df_high_hipertensao = df_high.loc[:, ['HipertensaoAlta', 'Diabéticos', 'Quantidade']].groupby(['HipertensaoAlta', 'Diabéticos']).sum().reset_index()
sns.barplot(df_high_hipertensao, x="Diabéticos", y="Quantidade", hue="HipertensaoAlta");

# ColesterolAlto
df_high_colesterol = df_high.loc[:, ['Diabéticos', 'ColesterolAlto', 'Quantidade', '5AnosColesterol']].groupby(['Diabéticos', 'ColesterolAlto', '5AnosColesterol']).sum().reset_index()

df_high_colesterol['Colesterol'] = df_high_colesterol.apply(lambda x:
    'Alto, verificado/5 Anos' if (x['ColesterolAlto'] == 'Sim' and x['5AnosColesterol'] == 'Sim')
    else 'Alto, não verificado/5 Anos' if (x['ColesterolAlto'] == 'Sim' and x['5AnosColesterol'] == 'Não')
    else 'Não alto, verificado/5 anos' if (x['ColesterolAlto'] == 'Não' and x['5AnosColesterol'] == 'Sim')
    else 'Não alto, não verificado/5 Anos', axis=1)


ax = sns.barplot(df_high_colesterol, x="Diabéticos", y="Quantidade", hue="Colesterol");
ax.bar_label(ax.containers[0], fontsize=10);
ax.bar_label(ax.containers[1], fontsize=10);
ax.bar_label(ax.containers[2], fontsize=10);
ax.bar_label(ax.containers[3], fontsize=10);

"""## Graficos IMC e Idade"""

df['Age'].value_counts()
# 1: 18-24 anos
# 2: 25-29 anos
# 3: 30-34 anos
# 4: 35-39 anos
# 5: 40-44 anos
# 6: 45-49 anos
# 7: 50-54 anos
# 8: 55-59 anos
# 9: 60-64 anos
# 10: 65-69 anos
# 11: 70-74 anos
# 12: 75-79 anos
# 13: 80 anos ou mais

# Graficos para os 'HipertensaoAlta', 'ColesterolAlto'
df_bmi = df.loc[:, ['BMI', 'Age', 'Diabetes_binary']];
df_bmi.columns = ['IMC', 'Age','Diabéticos'];

# Faz groupby
df_bmi['IMC'] = df_bmi['IMC'].apply(lambda x:
    'Abaixo' if x < 19
    else 'Saudável' if x < 25
    else 'Sobrepeso' if x < 30
    else 'Obesidade Leve' if x < 35
    else 'Obesidade Moderada' if x < 40
    else 'Obesidade Grave'
)

df_bmi = df_bmi.loc[:, ['IMC', 'Diabéticos']].groupby(['IMC']).sum().reset_index()

sns.barplot(df_bmi, x="IMC", y="Diabéticos");
# df_bmi

"""# DESC"""

# df.columns = ['Diabetico', 'HipertensaoAlta', 'ColesterolAlto', 'VerificacaoColesterol', 'IMC', 'Fumante', 'AVC', 'CardiacaAtaque', 'AtividadeFisica', 'Frutas', 'Vegetais', 'ConsumoPesadoAlcool', 'CuidadoDaSaúde', 'NoMedic12Meses', 'SaudeGeral', 'SaudeMental', 'SaudeFisica', 'DificAndarEscada', 'Sexo', 'Idade', 'Educação', 'Renda']

df_2classe.columns

df_2classe['DiffWalk'].value_counts()

df.dtypes

############ Diabetes_binary
#
# 0 = no diabetes
# 1 = prediabetes 2 = diabetes
#
############


############ HighBP ===> HipertensaoAlta
#
# 0 = no high BP
# 1 = high BP
#
############


############ HighChol ===> ColesterolAlto
#
# 0 = no high cholesterol
# 1 = high cholesterol
#
############


############ CholCheck ===> Colesterol verificado em 5 anos
#
# 0 = no cholesterol check in 5 years
# 1 = yes cholesterol check in 5 years
#
############


############ BMI ===> IMC **************************************************************************************************************
# IMC quanto maior, deve ser mais provavel TER diabetes? Verificar de acordo com a Idade ...
#
# Body Mass Index
#
############


############ Smoker ===> Fumante
#
# Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes]
# 0 = no
# 1 = yes
#
############


############ Stroke ===> AVC
#
# (Ever told) you had a stroke.
# 0 = no
# 1 = yes
#
############


############ HeartDiseaseorAttack ===> Ataque Cardíaco
#
# coronary heart disease (CHD) or myocardial infarction (MI)
# 0 = no
# 1 = yes
#
############


############ PhysActivity ===> Atividade fisica nos ultimos 30 dias?
# Atividade fisica, quem fez deve ter menos propensão de ter **************************************************************************************************************
# physical activity in past 30 days - not including job
# 0 = no
# 1 = yes
#
############


############ Fruits ===> Consome fruta 1 ou mais vezes ao dia?
# Quem como fruta, mais certo que não tenha **************************************************************************************************************
# Consume Fruit 1 or more times per day
# 0 = no
# 1 = yes
#
############


############ Veggies ===> Consome vegetal 1 ou mais vezes ao dia?
# Quem come vegetais provavelmente não tenha **************************************************************************************************************
# Consume Vegetables 1 or more times per day
# 0 = no
# 1 = yes
#
############


############ HvyAlcoholConsump ===> Se bebe muito: Homens mais de 14 vezes por semana e mulheres mais de 7 vezes por semana
# Quem bebe muito, pode desemvolver diabetes **************************************************************************************************************
# Heavy drinkers (adult men having more than 14 drinks per week and adult women having more than 7 drinks per week)
# 0 = no
# 1 = yes
#
############


############ AnyHealthcare ===> Ter qualquer tipo de cobertura de saúde, incluindo seguro saúde, planos pré-pagos como HMO, etc.
# Plano de saude, provavelmente não tem por ter cuidado ou tem para se cuidar **************************************************************************************************************
# Have any kind of health care coverage, including health insurance, prepaid plans such as HMO, etc.
# 0 = no
# 1 = yes
#
############


############ NoDocbcCost ===> Houve algum momento nos últimos 12 meses em que você precisou consultar um médico, mas não pôde por causa do custo?
# Possivelmente tem, pois já precisou ir ao medico **************************************************************************************************************
# Was there a time in the past 12 months when you needed to see a doctor but could not because of cost?
# 0 = no
# 1 = yes
#
############


############ GenHlth ===> Você diria que, em geral, sua saúde é: escala de 1 a 5?
# quanto maior, mais provavel ter **************************************************************************************************************
# Would you say that in general your health is: scale 1-5
# 1 = excellent
# 2 = very good
# 3 = good
# 4 = fair
# 5 = poor
#
############


############ MentHlth ===> Agora, pensando na sua saúde mental, que inclui estresse, depressão e problemas emocionais, por quantos dias durante os últimos 30 dias sua saúde mental não foi boa?
# Quanto maior, mais provavel ter **************************************************************************************************************
# Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health not good?
# scale 1-30 days
#
############


############ PhysHlth ===> Agora, pensando na sua saúde física, que inclui doenças e lesões físicas, durante quantos dias durante os últimos 30 dias a sua saúde física não foi boa?
# Quanto maior, mais provavel ter **************************************************************************************************************
# Now thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good?
# scale 1-30 days
#
############


############ DiffWalk ===> Você tem muita dificuldade para andar ou subir escadas?
# Quanto maior, mais provavel ter **************************************************************************************************************
# Do you have serious difficulty walking or climbing stairs?
# 0 = no
# 1 = yes
#
############


############ Sex => Sexo?
#
# 0 = female
# 1 = male
#
############


############ Age ===> Idade,  classificação de idade segundo _AGEG5YR
#
# 13-level age category (_AGEG5YR see codebook)
# 1 = 18-24
# 9 = 60-64
# 13 = 80 or older
#
############


############ Education ===> Educação
#
# Education level (EDUCA see codebook) scale 1-6
# 1 = Never attended school or only kindergarten
# 2 = Grades 1 through 8 (Elementary)
# 3 = Grades 9 through 11 (Some high school)
# 4 = Grade 12 or GED (High school graduate)
# 5 = College 1 year to 3 years (Some college or technical school)
# 6 = College 4 years or more (College graduate)
#
############


############ Incom ===> Escala de renda (INCOME2 ver livro de códigos) escala 1-8
#
# Income scale (INCOME2 see codebook) scale 1-8
# 1 = less than $10,000
# 5 = less than $35,000
# 8 = $75,000 or more
#
############

"""## TESTE"""

############ Diabetes_binary
#
# 0 = no diabetes
# 1 = prediabetes 2 = diabetes
#
############


############ HighBP ===> HipertensaoAlta
#
# 0 = no high BP
# 1 = high BP
#
############


############ HighChol ===> ColesterolAlto
#
# 0 = no high cholesterol
# 1 = high cholesterol
#
############


############ CholCheck ===> Colesterol verificado em 5 anos
#
# 0 = no cholesterol check in 5 years
# 1 = yes cholesterol check in 5 years
#
############


############ Smoker ===> Fumante
#
# Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes]
# 0 = no
# 1 = yes
#
############


############ Stroke ===> AVC
#
# (Ever told) you had a stroke.
# 0 = no
# 1 = yes
#
############


############ HeartDiseaseorAttack ===> Ataque Cardíaco
#
# coronary heart disease (CHD) or myocardial infarction (MI)
# 0 = no
# 1 = yes
#
############


############ Sex => Sexo?
#
# 0 = female
# 1 = male
#
############


############ Age ===> Idade,  classificação de idade segundo _AGEG5YR
#
# 13-level age category (_AGEG5YR see codebook)
# 1 = 18-24
# 9 = 60-64
# 13 = 80 or older
#
############


############ Education ===> Educação
#
# Education level (EDUCA see codebook) scale 1-6
# 1 = Never attended school or only kindergarten
# 2 = Grades 1 through 8 (Elementary)
# 3 = Grades 9 through 11 (Some high school)
# 4 = Grade 12 or GED (High school graduate)
# 5 = College 1 year to 3 years (Some college or technical school)
# 6 = College 4 years or more (College graduate)
#
############


############ Incom ===> Escala de renda (INCOME2 ver livro de códigos) escala 1-8
#
# Income scale (INCOME2 see codebook) scale 1-8
# 1 = less than $10,000
# 5 = less than $35,000
# 8 = $75,000 or more
#
############



"""# VERIFICAR PERGUNTAS

## Quanto maior, mais provavel ter
DiffWalk ===> Você tem muita dificuldade para andar ou subir escadas?
"""

# Diabeticos DiffWalk
df_fruta = df.loc[:, ['DiffWalk', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['AndarSubirEscadas', 'Age','Diabéticos'];
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta = df_fruta.loc[:, ['AndarSubirEscadas', 'Diabéticos']].reset_index().groupby(['AndarSubirEscadas', 'Diabéticos']).count().reset_index()

df_fruta['AndarSubirEscadas'] = df_fruta['AndarSubirEscadas'].map({1: 'Sim', 0: 'Não'});

df_fruta_sim = df_fruta[df_fruta['Diabéticos'] == 'Sim']
df_fruta_sim.columns = ['AndarSubirEscadas', 'Diabéticos', 'Quantidade'];

sns.barplot(df_fruta_sim, x="AndarSubirEscadas", y="Quantidade");

df_fruta_sim = df_fruta[df_fruta['Diabéticos'] == 'Não']
df_fruta_sim.columns = ['AndarSubirEscadas', 'Diabéticos', 'Quantidade'];

sns.barplot(df_fruta_sim, x="AndarSubirEscadas", y="Quantidade");

"""## Quanto maior, mais provavel ter
PhysHlth ===> Agora, pensando na sua saúde física, que inclui doenças e lesões físicas, durante quantos dias durante os últimos 30 dias a sua saúde física não foi boa?

"""

# Diabeticos PhysHlth
df_fruta = df.loc[:, ['PhysHlth', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['SaúdeFisica', 'Age','Diabéticos'];

df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta = df_fruta.loc[:, ['SaúdeFisica', 'Diabéticos']].reset_index().groupby(['SaúdeFisica', 'Diabéticos']).count().reset_index()

df_fruta_sim = df_fruta[df_fruta['Diabéticos'] == 'Sim']
df_fruta_sim.columns = ['SaúdeFisica', 'Diabéticos', 'Quantidade'];

sns.barplot(df_fruta_sim, x="SaúdeFisica", y="Quantidade");

df_fruta_sim = df_fruta[df_fruta['Diabéticos'] == 'Não']
df_fruta_sim.columns = ['SaúdeFisica', 'Diabéticos', 'Quantidade'];

sns.barplot(df_fruta_sim, x="SaúdeFisica", y="Quantidade");

"""## Quanto maior, mais provavel ter

MentHlth ===> Agora, pensando na sua saúde mental, que inclui estresse, depressão e problemas emocionais, por quantos dias durante os últimos 30 dias sua saúde mental não foi boa?
"""

# Diabeticos MentHlth
df_fruta = df.loc[:, ['MentHlth', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['SaúdeMental', 'Age','Diabéticos'];

df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta = df_fruta.loc[:, ['SaúdeMental', 'Diabéticos']].reset_index().groupby(['SaúdeMental', 'Diabéticos']).count().reset_index()

df_fruta_sim = df_fruta[df_fruta['Diabéticos'] == 'Sim']
df_fruta_sim.columns = ['SaúdeMental', 'Diabéticos', 'Quantidade'];

sns.barplot(df_fruta_sim, x="SaúdeMental", y="Quantidade");

df_fruta_sim = df_fruta[df_fruta['Diabéticos'] == 'Não']
df_fruta_sim.columns = ['SaúdeMental', 'Diabéticos', 'Quantidade'];

sns.barplot(df_fruta_sim, x="SaúdeMental", y="Quantidade");

"""## IMC quanto maior, deve ser mais provavel TER diabetes? Verificar de acordo com a Idade?

"""

df['Age']

df_bmi = df.loc[:, ['BMI', 'Age', 'Diabetes_binary']];
df_bmi.columns = ['IMC', 'Age','Diabéticos'];



# Faz groupby
df_bmi['IMC'] = df_bmi['IMC'].apply(lambda x:
    'Abaixo' if x < 19
    else 'Saudável' if x < 25
    else 'Sobrepeso' if x < 30
    else 'Obesidade Leve' if x < 35
    else 'Obesidade Moderada' if x < 40
    else 'Obesidade Grave'
)

df_bmi = df_bmi.loc[:, ['IMC', 'Diabéticos']].groupby(['IMC']).sum().reset_index()

sns.barplot(df_bmi, x="IMC", y="Diabéticos");
# df_bmi

"""## Atividade fisica, quem fez deve ter menos propensão de ter

"""

# Diabeticos que fazem atividade fisica
df_af = df.loc[:, ['PhysActivity', 'Age', 'Diabetes_binary']];
df_af.columns = ['AtividadeFisica', 'Age','Diabéticos'];

df_af['AtividadeFisica'] = df_af['AtividadeFisica']

df_af['AtividadeFisica'] = df_af['AtividadeFisica'].map({1: 'Sim', 0: 'Não'});
df_af['Diabéticos'] = df_af['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_af_1 = df_af[df_af['Diabéticos'] == 'Sim']

df_af_1 = df_af_1.loc[:, ['AtividadeFisica', 'Diabéticos']].groupby(['AtividadeFisica']).count().reset_index()
df_af_1
sns.barplot(df_af_1, x="AtividadeFisica", y="Diabéticos");

# Não Diabeticos que fazem atividade fisica
df_af = df.loc[:, ['PhysActivity', 'Age', 'Diabetes_binary']];
df_af.columns = ['AtividadeFisica', 'Age','Diabéticos'];

df_af['AtividadeFisica'] = df_af['AtividadeFisica']

df_af['AtividadeFisica'] = df_af['AtividadeFisica'].map({1: 'Sim', 0: 'Não'});
df_af['Diabéticos'] = df_af['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_af_1 = df_af[df_af['Diabéticos'] == 'Não']

df_af_1 = df_af_1.loc[:, ['AtividadeFisica', 'Diabéticos']].groupby(['AtividadeFisica']).count().reset_index()
df_af_1
sns.barplot(df_af_1, x="AtividadeFisica", y="Diabéticos");

"""## Quem como fruta, mais certo que não tenha"""

# Total que comem não comem frutas
df_fruta = df.loc[:, ['Fruits', 'Diabetes_binary']];
df_fruta.columns = ['Frutas', 'Diabéticos'];

df_fruta['Frutas'] = df_fruta['Frutas']

df_fruta['Frutas'] = df_fruta['Frutas'].map({1: 'Sim', 0: 'Não'});

df_fruta_1 = df_fruta.loc[:, ['Frutas', 'Diabéticos']].groupby(['Frutas']).count().reset_index()
df_fruta_1

# Diabeticos que comem frutas
df_fruta = df.loc[:, ['Fruits', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['Frutas', 'Age','Diabéticos'];

df_fruta['Frutas'] = df_fruta['Frutas']

df_fruta['Frutas'] = df_fruta['Frutas'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Sim']

df_fruta_1 = df_fruta_1.loc[:, ['Frutas', 'Diabéticos']].groupby(['Frutas']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="Frutas", y="Diabéticos");

# Não Diabeticos que comem frutas
df_fruta = df.loc[:, ['Fruits', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['Frutas', 'Age','Diabéticos'];

df_fruta['Frutas'] = df_fruta['Frutas']

df_fruta['Frutas'] = df_fruta['Frutas'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Não']

df_fruta_1 = df_fruta_1.loc[:, ['Frutas', 'Diabéticos']].groupby(['Frutas']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="Frutas", y="Diabéticos");

"""## Quem come vegetais provavelmente não tenha

"""

# Todos que comem Veggies ou não
df_fruta = df.loc[:, ['Veggies', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['Vegetais', 'Age','Diabéticos'];

df_fruta['Vegetais'] = df_fruta['Vegetais']

df_fruta['Vegetais'] = df_fruta['Vegetais'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});

df_fruta = df_fruta.loc[:, ['Vegetais', 'Diabéticos']].groupby(['Vegetais']).count().reset_index()
df_fruta

# Diabeticos que comem Veggies
df_fruta = df.loc[:, ['Veggies', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['Vegetais', 'Age','Diabéticos'];

df_fruta['Vegetais'] = df_fruta['Vegetais']

df_fruta['Vegetais'] = df_fruta['Vegetais'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Sim']

df_fruta_1 = df_fruta_1.loc[:, ['Vegetais', 'Diabéticos']].groupby(['Vegetais']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="Vegetais", y="Diabéticos");

# Não Diabeticos que comem Veggies
df_fruta = df.loc[:, ['Veggies', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['Vegetais', 'Age','Diabéticos'];

df_fruta['Vegetais'] = df_fruta['Vegetais']

df_fruta['Vegetais'] = df_fruta['Vegetais'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Não']

df_fruta_1 = df_fruta_1.loc[:, ['Vegetais', 'Diabéticos']].groupby(['Vegetais']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="Vegetais", y="Diabéticos");

"""## Quem bebe muito, pode desemvolver diabetes"""

# Diabeticos ConsumoÁlcool HvyAlcoholConsumo
df_fruta = df.loc[:, ['HvyAlcoholConsump', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['ConsumoÁlcool', 'Age','Diabéticos'];

df_fruta['ConsumoÁlcool'] = df_fruta['ConsumoÁlcool']

df_fruta['ConsumoÁlcool'] = df_fruta['ConsumoÁlcool'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});

df_fruta = df_fruta.loc[:, ['ConsumoÁlcool', 'Diabéticos']].groupby(['ConsumoÁlcool']).count().reset_index()
df_fruta

# Diabeticos ConsumoÁlcool HvyAlcoholConsumo
df_fruta = df.loc[:, ['HvyAlcoholConsump', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['ConsumoÁlcool', 'Age','Diabéticos'];

df_fruta['ConsumoÁlcool'] = df_fruta['ConsumoÁlcool']

df_fruta['ConsumoÁlcool'] = df_fruta['ConsumoÁlcool'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Sim']

df_fruta_1 = df_fruta_1.loc[:, ['ConsumoÁlcool', 'Diabéticos']].groupby(['ConsumoÁlcool']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="ConsumoÁlcool", y="Diabéticos");

# Diabeticos ConsumoÁlcool HvyAlcoholConsumo
df_fruta = df.loc[:, ['HvyAlcoholConsump', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['ConsumoÁlcool', 'Age','Diabéticos'];

df_fruta['ConsumoÁlcool'] = df_fruta['ConsumoÁlcool']

df_fruta['ConsumoÁlcool'] = df_fruta['ConsumoÁlcool'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Não']

df_fruta_1 = df_fruta_1.loc[:, ['ConsumoÁlcool', 'Diabéticos']].groupby(['ConsumoÁlcool']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="ConsumoÁlcool", y="Diabéticos");

"""## Plano de saude, provavelmente não tem por ter cuidado ou tem para se cuidar

"""

# Diabeticos PlanoSaúde HvyAlcoholConsumo
df_fruta = df.loc[:, ['AnyHealthcare', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['PlanoSaúde', 'Age','Diabéticos'];

df_fruta['PlanoSaúde'] = df_fruta['PlanoSaúde']

df_fruta['PlanoSaúde'] = df_fruta['PlanoSaúde'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});

df_fruta = df_fruta.loc[:, ['PlanoSaúde', 'Diabéticos']].groupby(['PlanoSaúde']).count().reset_index()
df_fruta

# Diabeticos PlanoSaúde HvyAlcoholConsumo
df_fruta = df.loc[:, ['AnyHealthcare', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['PlanoSaúde', 'Age','Diabéticos'];

df_fruta['PlanoSaúde'] = df_fruta['PlanoSaúde']

df_fruta['PlanoSaúde'] = df_fruta['PlanoSaúde'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Sim']

df_fruta_1 = df_fruta_1.loc[:, ['PlanoSaúde', 'Diabéticos']].groupby(['PlanoSaúde']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="PlanoSaúde", y="Diabéticos");

# Não Diabeticos PlanoSaúde HvyAlcoholConsumo
df_fruta = df.loc[:, ['AnyHealthcare', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['PlanoSaúde', 'Age','Diabéticos'];

df_fruta['PlanoSaúde'] = df_fruta['PlanoSaúde']

df_fruta['PlanoSaúde'] = df_fruta['PlanoSaúde'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Não']

df_fruta_1 = df_fruta_1.loc[:, ['PlanoSaúde', 'Diabéticos']].groupby(['PlanoSaúde']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="PlanoSaúde", y="Diabéticos");

"""## Possivelmente tem, pois já precisou ir ao medico
NoDocbcCost ===> Houve algum momento nos últimos 12 meses em que você precisou consultar um médico, mas não pôde por causa do custo?
"""

# Diabeticos FaltaDeDinheiro HvyAlcoholConsumo
df_fruta = df.loc[:, ['NoDocbcCost', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['FaltaDeDinheiro', 'Age','Diabéticos'];

df_fruta['FaltaDeDinheiro'] = df_fruta['FaltaDeDinheiro']

df_fruta['FaltaDeDinheiro'] = df_fruta['FaltaDeDinheiro'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Sim']

df_fruta_1 = df_fruta_1.loc[:, ['FaltaDeDinheiro', 'Diabéticos']].groupby(['FaltaDeDinheiro']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="FaltaDeDinheiro", y="Diabéticos");

# Não Diabeticos FaltaDeDinheiro HvyAlcoholConsumo
df_fruta = df.loc[:, ['NoDocbcCost', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['FaltaDeDinheiro', 'Age','Diabéticos'];

df_fruta['FaltaDeDinheiro'] = df_fruta['FaltaDeDinheiro']

df_fruta['FaltaDeDinheiro'] = df_fruta['FaltaDeDinheiro'].map({1: 'Sim', 0: 'Não'});
df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta_1 = df_fruta[df_fruta['Diabéticos'] == 'Não']

df_fruta_1 = df_fruta_1.loc[:, ['FaltaDeDinheiro', 'Diabéticos']].groupby(['FaltaDeDinheiro']).count().reset_index()
df_fruta_1
sns.barplot(df_fruta_1, x="FaltaDeDinheiro", y="Diabéticos");

"""## quanto maior, mais provavel ter
GenHlth ===> Você diria que, em geral, sua saúde é: escala de 1 a 5?

"""

# Diabeticos Saúde
df_fruta = df.loc[:, ['GenHlth', 'Age', 'Diabetes_binary']];
df_fruta.columns = ['Saúde', 'Age','Diabéticos'];

df_fruta['Saúde'] = df_fruta['Saúde']

df_fruta['Diabéticos'] = df_fruta['Diabéticos'].map({1: 'Sim', 0: 'Não'});
df_fruta = df_fruta.loc[:, ['Saúde', 'Diabéticos']].reset_index().groupby(['Saúde', 'Diabéticos']).count().reset_index()
df_fruta['Saúde'] = df_fruta['Saúde'].map({1: 'Excelente', 2: 'Muito Bom', 3: 'Bom', 4: 'Regular', 5: 'Ruim'});

df_fruta_sim = df_fruta[df_fruta['Diabéticos'] == 'Sim']
df_fruta_sim.columns = ['Saúde', 'Diabéticos', 'Quantidade'];

sns.barplot(df_fruta_sim, x="Saúde", y="Quantidade");

# Não Diabeticos Saúde
df_fruta_nao = df_fruta[df_fruta['Diabéticos'] == 'Não']
df_fruta_nao.columns = ['Saúde', 'Diabéticos', 'Quantidade'];

sns.barplot(df_fruta_nao, x="Saúde", y="Quantidade");

"""## OPA



"""

############ GenHlth ===> Você diria que, em geral, sua saúde é: escala de 1 a 5?
# quanto maior, mais provavel ter **************************************************************************************************************
# Would you say that in general your health is: scale 1-5
# 1 = excellent
# 2 = very good
# 3 = good
# 4 = fair
# 5 = poor
#
############


############ MentHlth ===> Agora, pensando na sua saúde mental, que inclui estresse, depressão e problemas emocionais, por quantos dias durante os últimos 30 dias sua saúde mental não foi boa?
# Quanto maior, mais provavel ter **************************************************************************************************************
# Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health not good?
# scale 1-30 days
#
############


############ PhysHlth ===> Agora, pensando na sua saúde física, que inclui doenças e lesões físicas, durante quantos dias durante os últimos 30 dias a sua saúde física não foi boa?
# Quanto maior, mais provavel ter **************************************************************************************************************
# Now thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good?
# scale 1-30 days
#
############


############ DiffWalk ===> Você tem muita dificuldade para andar ou subir escadas?
# Quanto maior, mais provavel ter **************************************************************************************************************
# Do you have serious difficulty walking or climbing stairs?
# 0 = no
# 1 = yes
#
############