import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


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


def insert_data_to_postgres(dataframe, table_name, env_path=".env"):
    """
    Insere dados de um DataFrame em uma tabela no PostgreSQL usando pandas e sqlalchemy.

    Args:
        dataframe (pd.DataFrame): DataFrame contendo os dados a serem inseridos.
        table_name (str): Nome da tabela onde os dados serão inseridos.
        env_path (str): Caminho para o arquivo .env. Default é '.env'.
    """
    try:

        external_database_url = build_external_database_url(env_path)

        engine = create_engine(external_database_url)

        if validate_postgresql_connection(engine):
            dataframe.to_sql(table_name, con=engine, if_exists="replace", index=False)
            print(f"Dados inseridos com sucesso na tabela {table_name}")
        else:
            print("Falha na validação da conexão com o PostgreSQL.")

    except Exception as e:
        print("Erro ao inserir dados no PostgreSQL:", e)


if __name__ == "__main__":
    # Exemplo de uso:
    dataframe = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    insert_data_to_postgres(dataframe, "nome_da_tabela")
