import os
import json
from pydantic import BaseModel, ValidationError
from pathlib import Path
from datetime import datetime
from models import Despesa
import pandas as pd
from typing import Type, List, Optional
from sqlalchemy import create_engine
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def read_and_validate_json(file_path: Path, model: Type[BaseModel]):
    """
    Lê um arquivo JSON do caminho especificado, valida seus dados usando um modelo Pydantic fornecido
    e retorna uma lista de instâncias do modelo.
    Args:
        file_path (Path): Caminho para o arquivo JSON a ser lido e validado.
        model (Type[BaseModel]): Classe Pydantic que define a estrutura esperada dos dados JSON.

    Returns:
        List[BaseModel] or None: Uma lista de instâncias do modelo Pydantic, se a validação for bem-sucedida.
        Retorna None se houver um erro de validação, exibindo uma mensagem de erro detalhada.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        try:
            items = [model(**item) for item in json_data]
            return items
        except ValidationError as e:
            print(f"Erro de validação no arquivo {file_path}: {e}")
            return None
        
def read_normalize_json(file_path):
    """
    Função que recebe um arquivo JSON e normaliza se necessário. 
    Args:
        file_path (str ou Path): Caminho do arquivo JSON.    
    Returns:
        pd.DataFrame: DataFrame com os dados do arquivo JSON.
    """
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        df = pd.json_normalize(data)
    elif isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        raise TypeError("Formato JSON não suportado. Deve ser uma lista ou um objeto JSON.")
    return df

def insert_data_to_postgres(dataframe, table_name):
    """
    Insere dados de um DataFrame em uma tabela no PostgreSQL usando pandas e sqlalchemy.

    Args:
        dataframe (pd.DataFrame): DataFrame contendo os dados a serem inseridos.
        table_name (str): Nome da tabela onde os dados serão inseridos.
    """
    try:
        EXTERNAL_DATABASE_URL = f"postgres://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOSTNAME')}:{os.getenv('PORT')}/{os.getenv('DATABASE')}"

        engine = create_engine(EXTERNAL_DATABASE_URL)
        
        # Inserir os dados no banco de dados PostgreSQL
        dataframe.to_sql(table_name, con=engine, if_exists='append', index=False)
        
        print(f"Dados inseridos com sucesso na tabela {table_name}")
        
    except Exception as e:
        print("Erro ao inserir dados no PostgreSQL:", e)
        
def build_external_database_url(env_path='.env'):
    """
    Constrói a URL do banco de dados externo PostgreSQL baseada nas variáveis de ambiente carregadas do arquivo .env.

    Args:
        env_path (str): Caminho para o arquivo .env. Default é '.env'.

    Returns:
        str: URL do banco de dados externo PostgreSQL.
    """
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv(env_path)

    # Obtém as variáveis de ambiente necessárias
    hostname = os.getenv('HOSTNAME')
    port = os.getenv('PORT')
    database = os.getenv('DATABASE')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    # Monta a URL do banco de dados externo PostgreSQL
    external_database_url = f"postgresql://{username}:{password}@{hostname}:{port}/{database}"

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
        # Tenta obter uma conexão com o PostgreSQL
        with engine.connect():
            print("Conexão com o PostgreSQL bem-sucedida!")
            return True
    except Exception as e:
        print(f"Erro na conexão com o PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    # Exemplo de utilização:
    env_path = '.env'  # Caminho para o arquivo .env
    external_database_url = build_external_database_url(env_path)
    
    # Cria a engine SQLAlchemy
    engine = create_engine(external_database_url)
    
    # Valida a conexão com o PostgreSQL
    validate_postgresql_connection(engine)