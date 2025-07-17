import streamlit as st
import requests
import pandas as pd
import time

@st.cache_data # Cache the data to avoid fetching it multiple times
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8') # Converte o DataFrame para CSV sem o índice

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon = "✅")
    time.sleep(7) # Exibe a mensagem de sucesso por 5 segundos
    sucesso.empty() # Limpa a mensagem de sucesso


st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns)) # Seleciona todas as colunas por padrão
    
st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique()) # Seleciona todos os produtos por padrão
with st.sidebar.expander('Categoria do produto'):
    categorias = st.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique()) # Seleciona todas as categorias por padrão
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0, 5000)) # Seleciona o intervalo de preços de 0 a 5000
with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0, 250, (0, 250)) # Seleciona o intervalo de frete de 0 a 250
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max())) # Seleciona o intervalo de datas entre a data mínima e máxima
with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique()) # Seleciona todos os vendedores por padrão
with st.sidebar.expander('Local da Compra'):
    local_compra = st.multiselect('Selecione o local', dados['Local da compra'].unique(), dados['Local da compra'].unique()) # Seleciona todos os locais por padrão
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra', 1, 5, value = (1, 5)) # Seleciona o intervalo de avaliações de 1 a 5
with st.sidebar.expander('Tipo de Pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique()) # Seleciona todos os tipos de pagamento por padrão
with st.sidebar.expander('Quantidade de parcelas'):
    parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1, 24)) # Seleciona o intervalo de parcelas de 1 a 24

# Filtros da base de dados    
query = '''
Produto in @produtos and \
@preco[0] <= Preço <= @preco[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedores and \
`Local da compra` in @local_compra and \
@avaliacao[0] <= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@parcelas[0] <= `Quantidade de parcelas` <= @parcelas[1]

'''
dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.')

st.markdown('Escreva um nome para o arquivo CSV que será baixado:')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility = 'collapsed', value = 'dados') # Definindo um valor padrão para o nome do arquivo
    nome_arquivo += '.csv'  # Adiciona a extensão .csv ao nome do arquivo
with coluna2:
    st.download_button('Fazer o download da tabela em csv', data = converte_csv(dados_filtrados), file_name = nome_arquivo, mime = 'text/csv', on_click = mensagem_sucesso)