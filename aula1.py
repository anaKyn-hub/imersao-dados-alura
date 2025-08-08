import pandas as pd
import pandas_config

df = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")

print(df.head(7)) 
print(df.info())
print(df.describe())
print(df.shape) #não tem parenteses porque é atributo, não método, sua saída mostra o número de linhas em seguida o número de colunas