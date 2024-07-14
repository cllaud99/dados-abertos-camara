# Projeto de Análise de Despesas dos Deputados

## Disclaimer

Este projeto tem o intuito exclusivo de estudos e visa demonstrar o uso de ferramentas modernas de engenharia de dados e técnicas de visualização de dados. Não é objetivo fazer qualquer juízo de valor sobre os deputados ou suas atividades. Como o projeto é utilizado para testar técnicas e recursos pode sofrer alterações a todo momento e não deve ser utilizado para acompanhamento dos deputados visto que não necessáriamente estara atualizado e/ou finalizado


## Objetivos do Projeto.

Este projeto visa realizar a extração, carga e transformação de dados abertos disponíveis no portal da Câmara dos Deputados ([acesse aqui][def]). Utilizando técnicas modernas de engenharia de dados e ferramentas como o dbt-core, buscamos normalizar os dados e estruturá-los conforme o star schema proposto por Kimball, adotando uma abordagem de ELT (Extração, Carga e Transformação). Projeto utilizado para estudos e ainda em validação dos dados/indicadores

## Arquitetura do Projeto

A imagem abaixo descreve a arquitetura escolhida para o projeto:
e pode ser acessada  [aqui][link_excalidraw]

![Arquitetura do Projeto][pics_arquitetura]

# Como rodar o projeto

## Via Docker

### Pré-requisitos: Docker instalado

1. Clone o repositório:
    ```bash
    git clone https://github.com/cllaud99/dados-abertos-camara.git
    ```
2. Acesse o projeto:
    ```bash
    cd dados-abertos-camara
    ```
3. Preencha corretamente as variáveis de ambiente em `.env-exemple`
4. Salve-as como `.env`
5. Altere a variável `sample_run` para `false` se você for rodar o conjunto inteiro dos dados. Deixe como `true` para rodar uma amostragem de 3 deputados.
6. `dbt_context`: Se for rodar o Postgres em uma imagem Docker containerizada, escreva `"network"`, caso contrário, `"host"`.
7. Inicie os contêineres:
    ```bash
    docker compose up --build
    ```

Você pode visualizar o banco criado acessando:
[http://localhost:5050/](http://localhost:5050/)

Preencha o `Host name/address` com `“db”` e o restante com suas variáveis de ambiente.

## Via Python

### Pré-requisitos

- Python
- Poetry
- Um SGBD de sua preferência
- Um servidor Postgres configurado

1. Clone o repositório:
    ```bash
    git clone https://github.com/cllaud99/dados-abertos-camara.git
    ```
2. Acesse o projeto:
    ```bash
    cd dados-abertos-camara
    ```
3. Preencha corretamente as variáveis de ambiente em `.env-exemple`
4. Salve-as como `.env`
5. Altere a variável `sample_run` para `false` se você for rodar o conjunto inteiro dos dados. Deixe como `true` para rodar uma amostragem de 3 deputados.
6. Inicie o CLI do Poetry:
    ```bash
    poetry shell
    ```
7. Rode o comando:
    ```bash
    task run
    ```

## Acessar o projeto Power BI

Você pode acessar o projeto Power BI abrindo o arquivo `reports/dados-camara-deputados.pbip` com o Power BI Desktop.

## Gerar a documentação dbt com a data lineage

1. Gere a documentação:
    ```bash
    dbt docs generate
    ```
2. Sirva a documentação:
    ```bash
    dbt docs serve
    ```

### Etapas do Projeto:

1. **Coleta de Dados**: Consumo dos dados da API pública da Câmara dos Deputados sobre despesas parlamentares.
2. **Ingestão e Armazenamento Inicial**: Inserção dos dados brutos na camada `landing_zone` em formato JSON.
3. **Armazenamento em Banco de Dados**: Carga dos dados para um banco de dados PostgreSQL.
4. **Transformações**: Transformação dos dados usando DBT (Data Build Tool) até atingir a camada `dbt_gold`.
5. **Visualização**: Desenvolvimento de um dashboard que apresente os gastos por partido e por deputado, além de características como idade, sexo e escolaridade dos deputados.







[def]: https://dadosabertos.camara.leg.br/swagger/api.html
[pics_arquitetura]: docs/pics/arquitetura/arquitetura.png
[link_excalidraw]: https://excalidraw.com/#json=NKgR1G1AzJzyYPe7QJzPV,XC42PV_brRMLC4sPSCVezQ
