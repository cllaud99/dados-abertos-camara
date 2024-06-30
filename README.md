# Projeto de Análise de Despesas dos Deputados

Este projeto tem como objetivo consumir dados públicos da API da Câmara dos Deputados que lista as despesas de cada parlamentar. Os dados são processados e transformados através de diversas camadas até serem apresentados em um dashboard com visualizações úteis.

## Objetivos do Projeto

1. **Coletar Dados**: Consumir dados da API pública da Câmara dos Deputados sobre despesas parlamentares.
2. **Ingestão e Armazenamento Inicial**: Inserir os dados em uma camada `landing_zone` no formato JSON.
3. **Armazenamento em Banco de Dados**: Ingerir os dados em um banco de dados PostgreSQL na camada `bronze`.
4. **Transformações**: Realizar várias transformações nos dados usando DBT (Data Build Tool) até atingir a camada `ouro`.
5. **Visualização**: Gerar um dashboard que exiba os gastos por partido, por deputado e características dos deputados como idade, sexo, escolaridade, etc.
6. **Análise Avançada (Futuro)**: Implementar a biblioteca LangChain para análises avançadas com LangChain e OpenAI.

## Tecnologias Utilizadas

- **Python**: Versão 3.12.2
- **Poetry**: Para gerenciamento de dependências
- **Pydantic**: Para validações de dados
- **DBT (Data Build Tool)**: Para transformações de dados
- **PostgreSQL**: Para armazenamento dos dados na camada `bronze`
- **MkDocs**: Para documentação

## Estrutura do Projeto

```plaintext
.
DADOS-ABERTOS-CAMARA
├── .venv
├── app
│   ├── data_ingestion.py
│   └── get_api_data.py
├── data
│   └── .env
├── .gitignore
├── .python-version
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Configuração do Ambiente

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/seu_usuario/seu_projeto.git
    cd seu_projeto
    ```

2. **Instale as dependências com Poetry**:
    ```bash
    poetry install
    ```

3. **Configure o banco de dados PostgreSQL**:
    - Crie um banco de dados PostgreSQL e configure as credenciais no arquivo `.env`.

4. **Execute as ingestões e transformações**:
    - Execute o script de ingestão de dados:
        ```bash
        poetry run python src/data_ingestion.py
        ```
    - Execute as transformações com DBT:
        ```bash
        cd dbt_project
        dbt run
        ```

## Utilização

- **Ingestão de Dados**: O script `data_ingestion.py` consome dados da API e salva na camada `landing_zone`.
- **Transformações**: As transformações são realizadas usando DBT, gerando as camadas `silver` e `gold`.
- **Visualização**: Os dados transformados são utilizados para gerar visualizações em um dashboard.



/home/devenv/.dbt/profiles.yml