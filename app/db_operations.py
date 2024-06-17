import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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
                        f"""
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

            print(f"Todas as tabelas no esquema {schema} foram apagadas com sucesso.")
    except Exception as e:
        print("Erro ao apagar as tabelas do esquema:", e)


def build_external_database_url(env_path=".env"):
    """
    Constrói a URL do banco de dados externo PostgreSQL baseada nas variáveis de ambiente carregadas do arquivo .env.

    Args:
        env_path (str): Caminho para o arquivo .env. Default é '.env'.

    Returns:
        str: URL do banco de dados externo PostgreSQL.
    """

    load_dotenv(env_path)

    hostname = os.getenv("HOSTNAME")
    port = os.getenv("PORT")
    database = os.getenv("DATABASE")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    external_database_url = (
        f"postgresql://{username}:{password}@{hostname}:{port}/{database}"
    )

    return external_database_url


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
            print("Conexão com o PostgreSQL bem-sucedida!")
            return True
    except Exception as e:
        print(f"Erro na conexão com o PostgreSQL: {e}")
        return False


def create_postgres_schema(engine, schema):
    """
    Cria um esquema no PostgreSQL se ele não existir.

    Args:
        engine (sqlalchemy.engine.Engine): Objeto Engine do SQLAlchemy.
        schema (str): Nome do esquema a ser criado.
    """
    with engine.connect() as connection:
        # Usar a conexão para executar diretamente a criação do esquema
        connection.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")


def insert_data_to_postgres(dataframe, table_name, engine, schema="landing_zone"):
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
            table_name, con=engine, schema=schema, if_exists="append", index=False
        )
        print(f"Dados inseridos com sucesso na tabela {schema}.{table_name}")
    except Exception as e:
        print("Erro ao inserir dados no PostgreSQL:", e)


if __name__ == "__main__":

    dataframe = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    env_path = ".env"

    external_database_url = build_external_database_url(env_path)

    # Criar o engine fora do loop
    engine = create_engine(external_database_url)

    # Validar a conexão uma vez
    if validate_postgresql_connection(engine):
        insert_data_to_postgres(dataframe, "nome_da_tabela", engine)
    else:
        print("Falha na validação da conexão com o PostgreSQL.")
