import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Type

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
    with open(file_path, "r", encoding="utf-8") as file:
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
    return df


if __name__ == "__main__":
    json_folder = Path("data/landing_zone/despesas")
    for file_path in json_folder.glob("*.json"):
        validated_items = read_and_validate_json(file_path, Despesa)
        if validated_items:
            df = pd.DataFrame([item.model_dump() for item in validated_items])
            print(f"Dados válidos no arquivo {file_path}:")
            print(df.head())  # Exemplo de como imprimir o DataFrame

            # Insere os dados validados no PostgreSQL usando pandas e sqlalchemy
            table_name = "despesas"  # Nome da tabela no PostgreSQL

        else:
            print(f"Dados inválidos no arquivo {file_path}")