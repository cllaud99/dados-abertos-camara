# Use a Python runtime as a base image
FROM python:3.11.5-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Crie o diretório de logs
RUN mkdir -p /app/logs
RUN mkdir -p /app/data

# Copie o arquivo de dependências (poetry.lock e pyproject.toml)
COPY pyproject.toml poetry.lock /app/

# Instale o Poetry e suas dependências
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copie o restante do código para o diretório de trabalho
COPY . /app

RUN cd dbt_dados_abertos_camara \
    && dbt deps

# Comandos a serem executados ao iniciar o contêiner
CMD ["task", "docker_run"]
