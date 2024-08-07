import json
import shutil
from pathlib import Path
from typing import List, Type

import pandas as pd
from loguru import logger
from pydantic import BaseModel, ValidationError

log_format = "logs/app_{time:YYYY-MM-DD}.log"
logger.add(sink=log_format, format="{time} {level} {message}", level="INFO")
logger.add(
    sink=log_format, format="{time} {level} {message}", level="ERROR", rotation="1 week"
)


def read_and_validate_json(file_path: Path, model: Type[BaseModel]) -> List[BaseModel]:
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
    try:
        with open(str(file_path), "r", encoding="utf-8") as file:
            json_data = json.load(file)

            if isinstance(json_data, list):
                items = [model(**item) for item in json_data]
            elif isinstance(json_data.get("dados"), list):
                items = [model(**item) for item in json_data["dados"]]
            elif isinstance(json_data.get("dados"), dict):
                items = [model(**json_data["dados"])]
            else:
                logger.error(f"Estrutura inválida no arquivo {file_path}.")
                return None

            return items

    except FileNotFoundError:
        logger.error(f"Arquivo '{file_path}' não encontrado.")
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON no arquivo {file_path}: {e}")
    except ValidationError as e:
        logger.error(f"Erro de validação no arquivo {file_path}: {e}")
        logger.error(f"Dados inválidos: {e.json()}")

    return None


def normalize_columns_with_json(df):
    """
    Tenta carregar o conteúdo de cada coluna do DataFrame como JSON e normaliza as colunas
    que contêm dicionários JSON em novas colunas no DataFrame.

    Args:
        df (pd.DataFrame): DataFrame contendo as colunas a serem normalizadas.

    Returns:
        pd.DataFrame: DataFrame atualizado com colunas normalizadas, se aplicável.
    """
    try:
        for column in df.columns:
            try:
                df[column] = df[column].apply(json.loads)
                if df[column].apply(type).eq(dict).all():
                    df_normalized = pd.json_normalize(df[column])
                    df = pd.concat([df.drop(columns=[column]), df_normalized], axis=1)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(
                    f"Erro ao carregar conteúdo da coluna {column} como JSON: {e}"
                )
                pass

        logger.info("Colunas normalizadas com sucesso.")
        return df

    except Exception as e:
        logger.error(f"Erro ao normalizar colunas com JSON: {e}")
        raise


def delete_folder(folder_path):
    """
    Deletes a folder and all its contents.

    Args:
    - folder_path (str): Path to the folder to be deleted.
    """
    try:
        shutil.rmtree(folder_path)
        print(f"Pasta '{folder_path}' e seu conteúdo foram deletados com sucesso.")
    except Exception as e:
        print(f"Erro ao deletar a pasta '{folder_path}': {e}")
