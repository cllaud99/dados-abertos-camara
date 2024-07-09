import os

import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Column, Integer, String, JSON, ARRAY
from loguru import logger

load_dotenv()


def drop_all_tables_in_schema(engine, schema):
    """
    Apaga todas as tabelas de um esquema específico no PostgreSQL.

    Args:
        engine (sqlalchemy.engine.Engine): Objeto Engine do SQLAlchemy.
        schema (str): Nome do esquema cujas tabelas serão apagadas.
    """
    try:
        with engine.connect() as connection:
            with connection.begin():
                result = connection.execute(
                    text(
                        """
                        SELECT tablename FROM pg_tables
                        WHERE schemaname = :schema
                        """
                    ),
                    {"schema": schema},
                )

                tables = result.fetchall()

                for table in tables:
                    connection.execute(
                        text(f'DROP TABLE IF EXISTS "{schema}"."{table[0]}" CASCADE;')
                    )

            logger.info(f"Todas as tabelas no esquema {schema} foram apagadas com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao apagar as tabelas do esquema {schema}: {e}")


def build_external_database_url(env_path=".env"):
    """
    Constrói a URL do banco de dados externo PostgreSQL baseada nas variáveis de ambiente carregadas do arquivo .env.

    Args:
        env_path (str): Caminho para o arquivo .env. Default é '.env'.

    Returns:
        str: URL do banco de dados externo PostgreSQL.
    """
    try:
        load_dotenv(env_path)

        hostname = os.getenv("HOSTNAME")
        port = os.getenv("PORT")
        database = os.getenv("DATABASE")
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")

        # Verifica se todas as variáveis de ambiente estão definidas
        if not all([hostname, port, database, username, password]):
            raise EnvironmentError("Variáveis de ambiente incompletas")

        external_database_url = (
            f"postgresql://{username}:{password}@{hostname}:{port}/{database}"
        )

        logger.info("URL do banco de dados externo PostgreSQL construída com sucesso.")

        return external_database_url
    except Exception as e:
        logger.error(f"Erro ao construir a URL do banco de dados externo PostgreSQL: {e}")
        raise


def validate_postgresql_connection(engine):
    """
    Valida a conexão com o PostgreSQL utilizando a engine SQLAlchemy fornecida.

    Args:
        engine (sqlalchemy.engine.base.Engine): Instância de engine SQLAlchemy.

    Returns:
        bool: True se a conexão for bem-sucedida, False caso contrário.
    """
    try:
        with engine.connect():
            logger.info("Conexão com o PostgreSQL bem-sucedida!")
            return True
    except Exception as e:
        logger.error(f"Erro na conexão com o PostgreSQL: {e}")
        return False


def create_postgres_schema(engine, schema):
    """
    Cria um esquema no PostgreSQL se ele não existir.

    Args:
        engine (sqlalchemy.engine.Engine): Objeto Engine do SQLAlchemy.
        schema (str): Nome do esquema a ser criado.
    """
    try:
        with engine.connect() as connection:
            # Executa a criação do esquema utilizando SQLAlchemy text
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

        logger.info(f"Esquema {schema} criado com sucesso no PostgreSQL.")
    except Exception as e:
        logger.error(f"Erro ao criar o esquema {schema} no PostgreSQL: {e}")
        raise


def insert_data_to_postgres(dataframe, table_name, engine, schema="public"):
    """
    Insere dados de um DataFrame em uma tabela no PostgreSQL usando pandas e sqlalchemy.

    Args:
        dataframe (pd.DataFrame): DataFrame contendo os dados a serem inseridos.
        table_name (str): Nome da tabela onde os dados serão inseridos.
        engine (sqlalchemy.engine.Engine): Objeto Engine do SQLAlchemy.
        schema (str): Nome do esquema onde a tabela está localizada.
    """
    try:
        dataframe.to_sql(
            table_name, con=engine, schema=schema, if_exists="replace", index=False
        )
        logger.info(f"Dados inseridos com sucesso na tabela {schema}.{table_name}")
    except Exception as e:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {e}")
        raise
