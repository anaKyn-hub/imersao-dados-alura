import pandas as pd
import pandas_config
import dicionario
import numpy as np

df = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")

linhas, colunas = df.shape[0], df.shape[1]
#shape não tem parenteses porque é atributo, não método

#Renomeações dos valores
dicionario.rename_level(df)
dicionario.rename_companySize(df)
dicionario.rename_remote(df)
dicionario.rename_emplType(df)

#---------------------------------------------------------------------------------
#Função que reune os métodos da aula 1
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
#---------------------------------------------------------------------------------
#Função que reune os métodos da aula 2
def mostrar_metodos2():
    print("\nSoma os valores ausentes e mostra em qual coluna se encontram:")
    print(df.isnull().sum())

    print("\nValores únicos da coluna ano e da coluna de localização das empresas:")
    print(df["work_year"].unique())
    print(df["company_location"].unique())

    print("\nLinhas em que os valores nulos aparecem:")
    print(df[df.isnull().any(axis=1)])

#print(mostrar_metodos2())
#---------------------------------------------------------------------------------

#Criação de um DataFrame sobre salários para testes com média e mediana
df_salarios = pd.DataFrame({
    'nome': ['Ana', 'João', 'Calos', 'Daniela', 'Ryanna'],
    'salario': [4000, np.nan, 5000, np.nan, 100000]
})

#Criação de nova coluna e preenchimento dos valores nulos com a média dos salários
df_salarios['salario_media'] = df_salarios['salario'].fillna(df_salarios['salario'].mean().round(2))

#O calculo de média pode contaminar os dados, pois se há um valor alto demais, os novos valores ficarão altos também, o que pode não ser uma realidade. A mediana mantém uma boa média não deixando o valor alto destoante contaminar os dados. É importante preencher dados ausentes pois se formos fazer uma média geral, esses dados ausentes de tornam 0 e podem puxar a média para baixo
df_salarios['salario_mediana'] = df_salarios['salario'].fillna(df_salarios['salario'].median())

print('\n', df_salarios, '\n')
#-------------------

#Criação de um DataFrame sobre temperaturas para testes em que média e mediana não fazem sentido
df_temperaturas = pd.DataFrame({
    'dia_semana': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'],
    'temperatura': [30, np.nan, np.nan, 28, 27]
})

#A função usa o valor da linha anterior para preencher, caso não tenha valor antes, a função não funcionará como esperado. Existem métodos como bfill que pega o valor de linhas seguintes
df_temperaturas['preenchido_ffill'] = df_temperaturas['temperatura'].ffill()

print(df_temperaturas, '\n')
#-------------------

#Criação de um DataFrame sobre cidades usando valores fixos para preenchimento
df_cidades = pd.DataFrame({
    'nome': ['Ana', 'João', 'Calos', 'Daniela', 'Ryanna'],
    'cidade': ['São Paulo', np.nan, 'Curitiba', np.nan, 'Belém']
})
df_cidades['cidade_preenchida'] = df_cidades['cidade'].fillna("Não informado")

print(df_cidades, '\n')
#---------------------------------------------------------------------------------
#Criação de uma cópia do df sem as linhas que possuem valores nulos
df_limpo = df.dropna()

#Alteração do tipo de dado do ano de float para int para melhor visualização
df_limpo = df_limpo.assign(work_year = df_limpo['work_year'].astype('int64'))

print(df_limpo.head(3))