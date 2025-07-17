# 📊 Dashboard de Vendas com Streamlit

Este repositório contém um dashboard interativo desenvolvido em Streamlit para visualização e análise de dados de vendas.

## 🌟 Visão Geral

Este projeto tem como objetivo principal fornecer uma ferramenta intuitiva para explorar dados de vendas, identificar tendências e obter insights valiosos. O dashboard é construído com Streamlit, permitindo uma interface de usuário rica e interativa diretamente no navegador.

## ✨ Funcionalidades

* **Visualização de Métricas Chave:** Exibe métricas importantes de vendas como total de vendas, lucros, quantidade vendida, etc.
* **Análise por Período:** Permite filtrar os dados por diferentes períodos (anual, mensal, semanal, etc.).
* **Segmentação de Dados:** Possibilidade de segmentar vendas por diferentes categorias (produtos, regiões, clientes, etc.).
* **Gráficos Interativos:** Utiliza bibliotecas como Plotly ou Matplotlib para criar gráficos dinâmicos e informativos.
* **[Adicione outras funcionalidades específicas do seu dashboard, ex: previsões, comparações, etc.]**

## 🚀 Como Executar o Projeto Localmente

Siga estes passos para configurar e rodar o dashboard na sua máquina local:

### Pré-requisitos

Certifique-se de ter o Python 3.x instalado.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/marisouzaent/dashboard_vendas.git](https://github.com/marisouzaent/dashboard_vendas.git)
    cd dashboard_vendas
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### Executando o Dashboard

Com o ambiente virtual ativado, execute o aplicativo Streamlit:

```bash
streamlit run Dashboard.py