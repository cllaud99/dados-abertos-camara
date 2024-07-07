# Projeto de Análise de Despesas dos Deputados

## Disclaimer

Este projeto tem o intuito exclusivo de estudos e visa demonstrar o uso de ferramentas modernas de engenharia de dados e técnicas de visualização de dados. Não é objetivo fazer qualquer juízo de valor sobre os deputados ou suas atividades. Como o projeto é utilizado para testar técnicas e recursos pode sofrer alterações a todos momentos e não deve ser utilizado para acompanhamento dos deputados viso que não necessáriamente estara atualizado e/ou finalizado


## Objetivos do Projeto

Este projeto visa realizar a extração, carga e transformação de dados abertos disponíveis no portal da Câmara dos Deputados ([acesse aqui][def]). Utilizando técnicas modernas de engenharia de dados e ferramentas como o dbt-core, buscamos normalizar os dados e estruturá-los conforme o star schema proposto por Kimball, adotando uma abordagem de ELT (Extração, Carga e Transformação). Projeto utilizado para estudos e ainda em validação dos dados/indicadores

### Etapas do Projeto:

1. **Coleta de Dados**: Consumo dos dados da API pública da Câmara dos Deputados sobre despesas parlamentares.
2. **Ingestão e Armazenamento Inicial**: Inserção dos dados brutos na camada `landing_zone` em formato JSON.
3. **Armazenamento em Banco de Dados**: Carga dos dados para um banco de dados PostgreSQL.
4. **Transformações**: Transformação dos dados usando DBT (Data Build Tool) até atingir a camada `gold`.
5. **Visualização**: Desenvolvimento de um dashboard que apresente os gastos por partido e por deputado, além de características como idade, sexo e escolaridade dos deputados.


### Especificação de Requisitos para Dashboard - Matriz Dimensão-Indicador

Este documento detalha a especificação de requisitos para o desenvolvimento de um dashboard destinado a simular uma análise dos gastos e o perfil dos deputados. O objetivo é criar uma ferramenta interativa que permita uma compreensão detalhada dos dados financeiros e demográficos. Seguindo os requisitos estipulados abaixo

### Dimensão e Indicadores

### Deputado
- **Total de gastos por deputado:** Deve exibir a soma dos gastos realizados por cada deputado.
- **Média de gastos por deputado:** Deve calcular a média dos gastos realizados pelos deputados, oferecendo uma visão geral do comportamento de despesas.
- **Total de despesas por tipo:** Necessário somar as despesas categorizadas por tipo (ex: passagens aéreas, manutenção de veículos), facilitando a identificação de onde os recursos são mais utilizados.
 **Sexo dos deputados (distribuição por gênero):** Proporção de deputados do sexo masculino e feminino, crucial para análises de diversidade de gênero.
- **Idade dos deputados (distribuição por faixa etária e média de idade):** Distribuição dos deputados por faixas etárias e cálculo da média de idade, fornecendo entendimento sobre a faixa etária predominante.
- **Ranking de deputados por despesas:** Listagem dos deputados ordenados pelo total de despesas, do maior para o menor.

### Partido
- **Total de gastos por partido:** Soma dos gastos realizados pelos deputados de cada partido, permitindo comparações entre os partidos.
- **Média de gastos por deputado no partido:** Média dos gastos realizados pelos deputados dentro de cada partido, proporcionando uma visão do comportamento de despesas dentro de cada grupo político.
- **Número de deputados por partido:** Quantidade de deputados em atividade que fazem parte de cada partido.
- **Média de idade dos deputados no partido:** Média de idade dos deputados em cada partido
- **Distribuição por gênero dos deputados:** Proporção de deputados do sexo masculino e feminino em cada partido, importante para análises de diversidade.
- **Distribuição educacional dos deputados no partido:** Formação educacional dos deputados por partido, permitindo entender o nível de instrução dentro dos grupos políticos.

### Estado
- **Total de gastos por estado:** Soma dos gastos realizados pelos deputados de cada estado, ajudando a identificar onde os recursos são mais gastos.
- **Média de gastos por deputado no estado:** Média dos gastos realizados pelos deputados dentro de cada estado, oferecendo uma visão regional do comportamento de despesas.
- **Número de deputados por estado:** Quantidade de deputados pertencentes a cada estado, crucial para dimensionar a representação política.
- **Distribuição por gênero dos deputados no estado:** Proporção de deputados do sexo masculino e feminino em cada estado, importante para análises de diversidade regional.
- **Distribuição educacional dos deputados no estado:** Formação educacional dos deputados por estado, permitindo entender o nível de instrução regional.

### Formação dos Deputados
- **Distribuição educacional dos deputados:** Nível de formação educacional dos deputados, distribuídos por diferentes categorias (ex: Ensino Fundamental, Médio, Superior, Pós-Graduação, Mestrado, Doutorado), fornecendo insights sobre o perfil educacional.

### Tipo de Despesa
- **Total de despesas por tipo:** Soma dos gastos realizados pelos deputados por cada tipo de despesa, essencial para identificar as categorias de maior consumo.
- **Distribuição percentual de despesas por tipo:** Porcentagem de cada tipo de despesa em relação ao total de despesas, útil para análises proporcionais.
- **Valor absoluto de despesas por tipo:** Valores absolutos de despesas para cada tipo de despesa, fornecendo uma visão clara dos montantes gastos.

## Observações Adicionais

- **Visualizações Gráficas:** Os dashboards devem utilizar várias visualizações gráficas, como gráficos de barras, gráficos de rosca, treemaps, e mapas geográficos para representar os dados de forma clara e intuitiva.
- **Filtros Dinâmicos:** Deve haver a possibilidade de filtrar dados por UF (Unidade Federativa) e partido para análises específicas.
- **Comparações Temporais:** Deve ser possível realizar a análise das despesas por períodos (mensais) para identificar tendências e picos de gastos.


### Tabela resumo

**Dimensão** | **Indicadores**
--- | ---
**Deputado** | - Total de gastos por deputado <br> - Média de gastos por deputado <br> - Total de despesas por tipo <br> - Sexo dos deputados (distribuição por gênero) <br> - Distribuição por faixa etária <br> - Ranking de deputados por despesas
**Partido** | - Total de gastos por partido <br> - Média de gastos por deputado no partido  <br> - Número de deputados por partido <br> - Média de idade dos deputados no partido <br> - Distribuição por gênero dos deputados <br> - Distribuição educacional dos deputados no partido
**Estado** | - Total de gastos por estado <br> - Média de gastos por deputado no estado <br> - Número total de despesas por estado <br> - Número de deputados por estado <br> - Distribuição por gênero dos deputados no estado <br> - Distribuição educacional dos deputados no estado
**Formação dos Deputados** | - Distribuição educacional dos deputados
**Tipo de Despesa** |  - Valor absoluto de despesas por tipo


## Arquitetura do Projeto

A imagem abaixo descreve a arquitetura escolhida para o projeto:

![Arquitetura do Projeto][pics_arquitetura]

## Tecnologias Utilizadas

- **Python**: Versão 3.12.2
- **Poetry**: Gerenciamento de dependências
- **Pydantic**: Validação de dados
- **DBT (Data Build Tool)**: Transformações de dados
- **PostgreSQL**: Armazenamento de dados
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

[def]: https://dadosabertos.camara.leg.br/swagger/api.html
[pics_arquitetura]: pics/arquitetura/arquitetura.png
