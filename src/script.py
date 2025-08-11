import pandas as pd
import pandas_config
import dicionario as dicionario
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry

# ----- Carregamento dos dados -----
#df = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")
df = pd.read_csv("dados_imersão25.csv") # Usa o dataframe na pasta raiz

# ----- Criação de variáveis com o valor das quantidades de linhas e colunas -----
linhas, colunas = df.shape[0], df.shape[1]
#shape não tem parenteses porque é atributo, não método

# ----- Renomeações dos valores de algumas tabelas -----
dicionario.rename_level(df)
dicionario.rename_companySize(df)
dicionario.rename_remote(df)
dicionario.rename_emplType(df)

# ----- Função que reune os métodos da aula 1 -----
def mostrar_metodos1():
    print("\nTabela até a 7° linha:")
    print(df.head(7)) 

    print("\nInformações sobre os tipos de dados:")
    print(df.info())

    print("\nDescrição dos dados dos números:")
    print(df.describe())

    print("\nDescrição dos dados de forma mais analítica:")
    print(df.describe(include="object"))

    print(f"\nLinhas: {linhas}, colunas: {colunas}")

    print("\nContagem de cada nível de experiência:")
    print(df["experience_level"].value_counts())

#print(mostrar_metodos1())

# ----- Função que reune os métodos da aula 2 -----
def mostrar_metodos2():
    print("\nSoma os valores ausentes e mostra em qual coluna se encontram:")
    print(df.isnull().sum())

    print("\nValores únicos da coluna ano e da coluna de localização das empresas:")
    print(df["work_year"].unique())
    print(df["company_location"].unique())

    print("\nLinhas em que os valores nulos aparecem:")
    print(df[df.isnull().any(axis=1)])

#print(mostrar_metodos2())

# ----- Função dos exemplos de DataFrames -----
def exemplo_df():
    # Criação de um DataFrame sobre salários para testes com média e mediana
    df_salarios = pd.DataFrame({
        'nome': ['Ana', 'João', 'Calos', 'Daniela', 'Ryanna'],
        'salario': [4000, np.nan, 5000, np.nan, 100000]
    })

    # Criação de nova coluna e preenchimento dos valores nulos com a média dos salários
    df_salarios['salario_media'] = df_salarios['salario'].fillna(df_salarios['salario'].mean().round(2))

    # O calculo de média pode contaminar os dados, pois se há um valor alto demais, os novos valores ficarão altos também, o que pode não ser uma realidade. A mediana mantém uma boa média não deixando o valor alto destoante contaminar os dados. É importante preencher dados ausentes pois se formos fazer uma média geral, esses dados ausentes de tornam 0 e podem puxar a média para baixo
    df_salarios['salario_mediana'] = df_salarios['salario'].fillna(df_salarios['salario'].median())

    print('\n', df_salarios, '\n')
    #-------------------

    # Criação de um DataFrame sobre temperaturas para testes em que média e mediana não fazem sentido
    df_temperaturas = pd.DataFrame({
        'dia_semana': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'],
        'temperatura': [30, np.nan, np.nan, 28, 27]
    })

    # A função usa o valor da linha anterior para preencher, caso não tenha valor antes, a função não funcionará como esperado. Existem métodos como bfill que pega o valor de linhas seguintes
    df_temperaturas['preenchido_ffill'] = df_temperaturas['temperatura'].ffill()

    print(df_temperaturas, '\n')
    #-------------------

    # Criação de um DataFrame sobre cidades usando valores fixos para preenchimento
    df_cidades = pd.DataFrame({
        'nome': ['Ana', 'João', 'Calos', 'Daniela', 'Ryanna'],
        'cidade': ['São Paulo', np.nan, 'Curitiba', np.nan, 'Belém']
    })
    df_cidades['cidade_preenchida'] = df_cidades['cidade'].fillna("Não informado")

    print(df_cidades, '\n')
    #--------------------------------------------------------

#print(exemplo_df())

# ----- Criação de uma cópia do df sem as linhas que possuem valores nulos e convertendo o tipo de dado do ano -----
df_limpo = df.dropna()

#Alteração do tipo de dado do ano de float para int para melhor visualização
df_limpo = df_limpo.assign(work_year = df_limpo['work_year'].astype('int64'))

print(df_limpo.head(3))

# ----- Função que reune a criação dos gráficos estáticos -----
def graph_est():
    ordem = df_limpo.groupby('experience_level')['salary_in_usd'].mean().sort_values(ascending=True).index #ordena do maior pro menor

    # Visualização dos dados em gráficos de barras
    df_limpo['experience_level'].value_counts().plot(kind='bar', title='Distribuição de Cargos')
    plt.show() # Abre o gráfico em uma janela separada

    plt.figure(figsize=(8,5))
    sns.barplot(data=df_limpo, x='experience_level', y='salary_in_usd', order=ordem)
    plt.title('Relação de salário e Nível de Experiência')
    plt.xlabel("Nível de Experiência")
    plt.ylabel("Salário médio anual em USD")
    plt.show()

    # Histograma
    plt.figure(figsize=(8,5))
    sns.histplot(df_limpo['salary_in_usd'], bins= 80, kde=True)
    plt.title('Distribuição dos salários anuais')
    plt.xlabel("Salário em USD")
    plt.ylabel("Frequência")
    plt.show()

    # Bloxplot
    plt.figure(figsize=(8,5))
    sns.boxplot(x=df_limpo['salary_in_usd'])
    plt.title('Boxplot: Salário')
    plt.xlabel("Salário em USD")
    plt.show()

    # Bloxplot separando os níveis de experiência
    ordem_cargos = ['Junior', 'Pleno', 'Senior', 'Executive']
    plt.figure(figsize=(8,5))
    sns.boxplot(x='experience_level', y='salary_in_usd', data=df_limpo, order=ordem_cargos, palette='Set2', hue='experience_level')
    plt.title('Boxplot: Distribuição por nível de Experiência')
    plt.xlabel("Nível de Experiência")
    plt.ylabel("Salário em USD")
    plt.show()

#print(graph_est())

# ----- Função que reune a criação dos gráficos interativos -----
def graph_int():
    # Gráfico de torta
    remote_count = df_limpo['remote_ratio'].value_counts().reset_index()
    remote_count.columns = ['tipo_trabalho', 'quantidade']

    fig = px.pie(remote_count, 
                 names='tipo_trabalho',
                 values='quantidade',
                 title='Proporção dos tipos de trabalho')
    fig.update_traces(textinfo='percent+label')
    fig.show() #mostra como json e não como imagem por conta de não ser um notebook

    # Gráfico de rosquinha
    fig = px.pie(remote_count, 
                 names='tipo_trabalho',
                 values='quantidade',
                 title='Proporção dos tipos de trabalho')
    fig.update_traces(textinfo='percent+label')
    fig.show() #mostra como json e não como imagem por conta de não ser um notebook

#print(graph_int())

# ----- Desafio -----
#Criar um gráfico de salário por país dos cientistas de dados
def graph_desafio():
    df_cience = df_limpo[df_limpo['job_title'] == 'Data Scientist']
    ordemc = df_cience.groupby('company_location')['salary_in_usd'].mean().sort_values(ascending=True).index 

    plt.figure(figsize=(15,5))
    sns.barplot(data=df_cience, x='company_location', y='salary_in_usd', palette='Set2', order=ordemc)
    plt.title('Salário de Cientistas de Dados por Localização da Empresa')
    plt.xlabel("Localização da Empresa")
    plt.ylabel("Salário médio anual em USD")
    plt.show()

print(graph_desafio())

# ----- Conversão dos valores da coluna employee_residence e company location de iso2 para iso3 e criação de novas colunas com essas conversões -----
#Função para converter ISO-2 para ISO-3
def iso2_to_iso3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None

# Criar nova coluna com código ISO-3
df_limpo['residence_iso3'] = df_limpo['employee_residence'].apply(iso2_to_iso3)
df_limpo['company_location_iso3'] = df_limpo['company_location'].apply(iso2_to_iso3)

# ----- Baixa o DataFrame original com as modificações -----
#df_limpo.to_csv('dados_imersão25.csv', index=False)