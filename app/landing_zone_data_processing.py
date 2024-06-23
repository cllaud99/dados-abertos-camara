import json
from pathlib import Path
from typing import Type

import pandas as pd
from models import Despesa
from pydantic import BaseModel, ValidationError


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
    try:
        with open(str(file_path), "r", encoding="utf-8") as file:
            json_data = json.load(file)

            # Caso 1: JSON é uma lista de objetos
            if isinstance(json_data, list):
                try:
                    items = [model(**item) for item in json_data]
                    return items
                except ValidationError as e:
                    print(f"Erro de validação no arquivo {file_path}: {e}")
                    return None

            # Caso 2: Objeto com chave 'dados' contendo lista
            elif isinstance(json_data.get("dados"), list):
                try:
                    items = [model(**item) for item in json_data["dados"]]
                    return items
                except ValidationError as e:
                    print(f"Erro de validação no arquivo {file_path}: {e}")
                    return None

            # Caso 3: Objeto com chave 'dados' que não é lista
            elif isinstance(json_data.get("dados"), dict):
                try:
                    items = [model(**json_data["dados"])]
                    return items
                except ValidationError as e:
                    print(f"Erro de validação no arquivo {file_path}: {e}")
                    return None
        print(f"Estrutura inválida no arquivo {file_path}.")
        return None

    except FileNotFoundError:
        print(f"Arquivo '{file_path}' não encontrado.")
        return None
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None
    except ValidationError as e:
        print("Erro de validação:")
        print(e.json())
        return None


def normalize_columns_with_json(df):
    for column in df.columns:
        try:
            # Tentar carregar o conteúdo da coluna como JSON
            df[column] = df[column].apply(json.loads)
            
            # Normalizar apenas se o conteúdo for um dicionário
            if df[column].apply(type).eq(dict).all():
                df_normalized = pd.json_normalize(df[column])
                df = pd.concat([df.drop(columns=[column]), df_normalized], axis=1)
        except (json.JSONDecodeError, ValueError):
            # Ignorar a coluna se não puder ser carregada como JSON
            pass
    
    return df
