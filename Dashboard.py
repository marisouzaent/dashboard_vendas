import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout = 'wide')

def formata_numero(valor, prefixo = ''):
    """
    Formata um número para o padrão brasileiro (R$ 1.000,00)
    """
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:,.2f} {unidade}'
        valor /=1000
    return f'{prefixo} {valor:,.2f} milhões'
# Configurações do Streamlit

st.title("DASHBOARD DE VENDAS 🛒")

url = 'https://labdados.com/produtos'
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']

st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)

if regiao == 'Brasil':
    regiao = ''
    
todos_anos = st.sidebar.checkbox('Dados de todo o período', value = True) #cria um checkbox para selecionar todos os anos
if todos_anos:
    ano = ''
else:
    ano = st.sidebar.slider('Ano', 2020, 2023)


query_string = {'regiao':regiao.lower(), 'ano': ano} #cria um dicionário com os parâmetros da requisição
response = requests.get(url, params = query_string) #faz a requisição para a API
dados = pd.DataFrame.from_dict(response.json()) #transforma a requisição em json, e o json em dataframe
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y') #transforma a data em datetime

filtro_vendedores = st.sidebar.multiselect('Vendedores', dados['Vendedor'].unique())
if filtro_vendedores:
    dados = dados[dados['Vendedor'].isin(filtro_vendedores)] #filtra os dados pelos vendedores selecionados

##Tabelas
###Tabelas de receita
receita_estados = dados.groupby('Local da compra')[['Preço']].sum() # Agrupa os dados por estado e soma os preços
receita_estados = dados.drop_duplicates(subset = 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index= True).sort_values('Preço', ascending = False) #remove os duplicados, e faz o merge com a receita dos estados

receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq = 'ME'))['Preço'].sum().reset_index() # Agrupa os dados por mês e soma os preços
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year # Cria uma coluna com o ano
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name() # Cria uma coluna com o mês

receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending= False) # Agrupa os dados por categoria e soma os preços

###Tabelas de quantidade de vendas
vendas_estados = pd.DataFrame(dados.groupby('Local da compra')['Preço'].count()) # Agrupa os dados por estado e conta os preços
vendas_estados = dados.drop_duplicates(subset = 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(vendas_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending = False)

vendas_mensal = pd.DataFrame(dados.set_index('Data da Compra').groupby(pd.Grouper(freq = 'ME'))['Preço'].count()).reset_index()
vendas_mensal['Ano'] = vendas_mensal['Data da Compra'].dt.year # Cria uma coluna com o ano
vendas_mensal['Mes'] = vendas_mensal['Data da Compra'].dt.month_name() # Cria uma coluna com o mês

vendas_categorias = pd.DataFrame(dados.groupby('Categoria do Produto')['Preço'].count().sort_values(ascending = False)) # Agrupa os dados por categoria e conta os preços

###Tabelas vendedores
vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))

##Gráficos
fig_mapa_receita = px.scatter_geo(receita_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  size = 'Preço',
                                  template = 'seaborn',
                                  hover_name = 'Local da compra',
                                  hover_data = {'lat': False, 'lon': False},
                                  title = 'Receita por estado')

fig_receita_mensal = px.line(receita_mensal,
                             x = 'Mes',
                             y = 'Preço',
                             markers = True,
                             range_y = (0, receita_mensal.max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Receita mensal')

fig_receita_mensal.update_layout(yaxis_title = 'Receita')

fig_receita_estados = px.bar(receita_estados.head(),
                             x = 'Local da compra',
                             y =  'Preço',
                             text_auto = True,
                             title = 'Top estados (receita)'                            
                             )

fig_receita_estados.update_layout(yaxis_title = 'Receita')

fig_receita_categorias = px.bar(receita_categorias,
                               text_auto = True,
                               title = 'Receitas por categoria')

fig_receita_categorias.update_layout(yaxis_title = 'Receita')

fig_mapa_vendas = px.scatter_geo(vendas_estados,
                                 lat = 'lat',
                                 lon = 'lon',
                                 scope = 'south america',
                                 #fitbounds = 'locations',
                                 template = 'seaborn',
                                 size = 'Preço',
                                 hover_name = 'Local da compra',
                                 hover_data = {'lat': False, 'lon': False},
                                 title = 'Vendas por estado')

fig_vendas_mensal = px.line(vendas_mensal, 
              x = 'Mes',
              y='Preço',
              markers = True, 
              range_y = (0,vendas_mensal.max()), 
              color = 'Ano', 
              line_dash = 'Ano',
              title = 'Quantidade de vendas mensal')

fig_vendas_mensal.update_layout(yaxis_title='Quantidade de vendas')

fig_vendas_estados = px.bar(vendas_estados.head(),
                             x ='Local da compra',
                             y = 'Preço',
                             text_auto = True,
                             title = 'Top 5 estados'
)

fig_vendas_estados.update_layout(yaxis_title='Quantidade de vendas')

fig_vendas_categorias = px.bar(vendas_categorias, 
                                text_auto = True,
                                title = 'Vendas por categoria')
fig_vendas_categorias.update_layout(showlegend=False, yaxis_title='Quantidade de vendas')

## Visualizacao no streamlit
aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores']) #cria as abas

with aba1:
    coluna1, coluna2 = st.columns(2) #cria duas colunas
    with coluna1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$')) #mostra a receita total
        st.plotly_chart(fig_mapa_receita, use_container_width = True) #mostra o gráfico do mapa
        st.plotly_chart(fig_receita_estados, use_container_width = True)
    with coluna2:
        st.metric('Quantidade de Vendas', formata_numero(dados.shape[0])) #mostra a quantidade de vendas, o shape[0] é o número de linhas e colunas do dataframe
        st.plotly_chart(fig_receita_mensal, use_container_width = True) #mostra o gráfico de receita mensal
        st.plotly_chart(fig_receita_categorias, use_container_width = True)

with aba2:
    coluna1, coluna2 = st.columns(2) #cria duas colunas
    with coluna1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$')) #mostra a receita total
        st.plotly_chart(fig_mapa_vendas, use_container_width = True)
        st.plotly_chart(fig_vendas_estados, use_container_width = True)

    with coluna2:
        st.metric('Quantidade de Vendas', formata_numero(dados.shape[0])) #mostra a quantidade de vendas, o shape[0] é o número de linhas e colunas do dataframe
        st.plotly_chart(fig_vendas_mensal, use_container_width = True) #mostra o gráfico de receita mensal
        st.plotly_chart(fig_vendas_categorias, use_container_width = True)
        
with aba3:
    qtd_vendedores = st.number_input('Quantidade de vendedores', 2, 10, 5) #cria um input para a quantidade de vendedores
    coluna1, coluna2 = st.columns(2) #cria duas colunas
    with coluna1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$')) #mostra a receita total
        fig_receita_vendedores = px.bar(vendedores[['sum']].sort_values('sum', ascending = False).head(qtd_vendedores),
                                        x = 'sum',
                                        y = vendedores[['sum']].sort_values('sum', ascending = False).head(qtd_vendedores).index,
                                        text_auto = True,
                                        title = f'Top {qtd_vendedores} vendedores (receita)')
        st.plotly_chart(fig_receita_vendedores)

    with coluna2:
        st.metric('Quantidade de Vendas', formata_numero(dados.shape[0])) #mostra a quantidade de vendas, o shape[0] é o número de linhas e colunas do dataframe
        fig_vendas_vendedores = px.bar(vendedores[['count']].sort_values('count', ascending = False).head(qtd_vendedores),
                                        x = 'count',
                                        y = vendedores[['count']].sort_values('count', ascending = False).head(qtd_vendedores).index,
                                        text_auto = True,
                                        title = f'Top {qtd_vendedores} vendedores (quantidade de vendas)')
        st.plotly_chart(fig_vendas_vendedores)

#st.dataframe(dados)