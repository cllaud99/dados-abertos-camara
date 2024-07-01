# Projeto de Análise de Despesas dos Deputados

## Objetivos do Projeto

Este projeto visa realizar a extração, carga e transformação de dados abertos disponíveis no portal da Câmara dos Deputados ([acesse aqui][def]). Utilizando técnicas modernas de engenharia de dados e ferramentas como o dbt-core, buscamos normalizar os dados e estruturá-los conforme o star schema proposto por Kimball, adotando uma abordagem de ELT (Extração, Carga e Transformação).

### Etapas do Projeto:

1. **Coleta de Dados**: Consumo dos dados da API pública da Câmara dos Deputados sobre despesas parlamentares.
2. **Ingestão e Armazenamento Inicial**: Inserção dos dados brutos na camada `landing_zone` em formato JSON.
3. **Armazenamento em Banco de Dados**: Carga dos dados para um banco de dados PostgreSQL na camada `bronze`.
4. **Transformações**: Transformação dos dados usando DBT (Data Build Tool) até atingir a camada `gold`.
5. **Visualização**: Desenvolvimento de um dashboard que apresente os gastos por partido e por deputado, além de características como idade, sexo e escolaridade dos deputados.

## Matriz de Dimensão Indicador

### Objetivo: Responder as seguintes perguntas em um dashboard interativo:

| Dimensão            | Indicadores                                             |
|---------------------|---------------------------------------------------------|
| **Deputado**        | Total de gastos por deputado                            |
|                     | Média de gastos por deputado                            |
|                     | Total de despesas por tipo                              |
|                     | Sexo dos deputados (distribuição por gênero)            |
| **Partido**         | Total de gastos por partido                             |
|                     | Média de gastos por deputado no partido                 |
|                     | Número total de despesas por partido                    |
|                     | Número de deputados por partido                         |
|                     | Média de idade dos deputados no partido                 |
|                     | Distribuição por gênero dos deputados                   |
|                     | Distribuição educacional dos deputados no partido       |
| **Estado**          | Total de gastos por estado                              |
|                     | Média de gastos por deputado no estado                  |
|                     | Número total de despesas por estado                     |
| **Formação dos Deputados** | Distribuição educacional dos deputados           |

Esta matriz define os principais indicadores que serão desenvolvidos e visualizados no projeto, fornecendo uma estrutura clara das análises a serem realizadas.

## Arquitetura do Projeto

A imagem abaixo descreve a arquitetura escolhida para o projeto:

![Arquitetura do Projeto][pics_arquitetura]

## Tecnologias Utilizadas

- **Python**: Versão 3.12.2
- **Poetry**: Gerenciamento de dependências
- **Pydantic**: Validação de dados
- **DBT (Data Build Tool)**: Transformações de dados
- **PostgreSQL**: Armazenamento de dados na camada `bronze`
- **MkDocs**: Documentação

## Configuração do Ambiente

1. **Clone o repositório**:
    ```
    git clone https://github.com/cllaud99/dados-abertos-camara.git
    cd dados-abertos-camara
    ```

2. **Instale as dependências com Poetry**:
    ```
    poetry install
    ```

3. **Configure o banco de dados PostgreSQL**:
    - Crie um banco de dados PostgreSQL e configure as credenciais no arquivo `.env`.

4. **Execute as ingestões e transformações**:
    - Execute o script de ingestão de dados:
        ```
        poetry run python src/data_ingestion.py
        ```
    - Execute as transformações com DBT:
        ```
        cd dbt_project
        dbt run
        ```

## Utilização

- **Ingestão de Dados**: O script `data_ingestion.py` consome dados da API e salva na camada `landing_zone`.
- **Transformações**: As transformações são realizadas usando DBT, gerando as camadas `silver` e `gold`.
- **Visualização**: Os dados transformados são utilizados para gerar visualizações em um dashboard.

## Disclaimer

Este projeto tem o intuito exclusivo de estudar e demonstrar o uso de ferramentas modernas de engenharia de dados. Não é nosso objetivo fazer qualquer juízo de valor sobre os deputados ou suas atividades.

[def]: https://dadosabertos.camara.leg.br/swagger/api.html
[pics_arquitetura]: pics/arquitetura.png
