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
                    # Criar uma lista com um único objeto do modelo Pydantic
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
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        df = pd.json_normalize(data)
    elif isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        raise TypeError(
            "Formato JSON não suportado. Deve ser uma lista ou um objeto JSON."
        )

    df["file_name"] = Path(file_path).name

    print(df)

    return df
