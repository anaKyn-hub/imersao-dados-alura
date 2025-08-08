import pandas as pd
import pandas_config
import dicionario

df = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")

linhas, colunas = df.shape[0], df.shape[1]
#shape não tem parenteses porque é atributo, não método

#Renomeações dos valores
dicionario.rename_level(df)
dicionario.rename_companySize(df)
dicionario.rename_remote(df)
dicionario.rename_emplType(df)

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