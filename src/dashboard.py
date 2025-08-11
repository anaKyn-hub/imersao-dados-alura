import streamlit as st
import pandas as pd
import plotly.express as px
import pandas_config as pdconfig
import dicionario as dicionario

# ----- Carregamento dos dados -----
df = pd.read_csv("dados_imersão25.csv")

# ----- Renomeações dos valores de algumas tabelas -----
dicionario.rename_level(df)
dicionario.rename_companySize(df)
dicionario.rename_remote(df)
dicionario.rename_emplType(df)

# ----- Configuração da página web -----
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide" #ocupa a largura inteira, página larga
)

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df['work_year'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Nível de Experiência
nivexp_disponiveis = sorted(df['experience_level'].unique())
nivexp_selecionadas = st.sidebar.multiselect("Níveis de Experiência", nivexp_disponiveis, default=nivexp_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['employment_type'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['company_size'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# ----- Filtragem do DataFrame -----
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['work_year'].isin(anos_selecionados)) &
    (df['experience_level'].isin(nivexp_selecionadas)) &
    (df['employment_type'].isin(contratos_selecionados)) &
    (df['company_size'].isin(tamanhos_selecionados))
]

# ----- Conteúdo Principal da Página -----
st.title("Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# ----- Métricas Principais (KPIs) -----
st.subheader("Métricas Gerais (Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['salary_in_usd'].mean()
    salario_maximo = df_filtrado['salary_in_usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["job_title"].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""
    #Se não houver um dataframe ou ocorrer um problema, será retornado valores vazios

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

# ----- Análises Visuais com Gráficos e Plotly -----
st.subheader("Gráficos")

#Criação de duas colunas para os dois primeiros gráficos
col_graf1, col_graf2 = st.columns(2)

#Coluna 1 que contém o primeiro gráfico
with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('job_title')['salary_in_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='salary_in_usd',
            y='job_title',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'salary_in_usd': 'Média salarial anual (USD)', 'job_title': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

#Coluna 2 que contém o segundo gráfico
with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='salary_in_usd',
            nbins=50,
            title="Distribuição de salários anuais",
            labels={'salary_in_usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

#Criação de outras duas colunas para ficar abaixo das duas primeiras
col_graf3, col_graf4 = st.columns(2)

#Coluna 1 da segunda linha que contém o terceiro gráfico
with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remote_ratio'].value_counts().reset_index()
        remoto_contagem.columns = ['employment_type', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='employment_type',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

#Coluna 2 da segunda linha que contém o quarto gráfico
with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['job_title'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('company_location_iso3')['salary_in_usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='company_location_iso3',
            color='salary_in_usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país das empresas',
            labels={'salary_in_usd': 'Salário médio (USD)', 'company_location_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.") 

# ----- Tabela de Dados Detalhados -----
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado) #usa o dataframe filtrado e não o completo