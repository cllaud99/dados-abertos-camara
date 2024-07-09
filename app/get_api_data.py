import json
import os
from loguru import logger

import requests

log_format = "{time:YYYY-MM-DD_HH-mm-ss}_{level}.log"
logger.configure(handlers=[{"sink": log_format, "format": "{time} {message}"}])


def fetch_data(url, params=None):
    """
    Busca dados a partir da URL fornecida com cabeçalhos e parâmetros opcionais.
    Args:
        url (str): URL da qual os dados serão buscados.
        params (dict, opcional): Parâmetros opcionais para a requisição GET. Default é None.

    Returns:
        dict or None: Dados da resposta JSON se a requisição for bem-sucedida, None caso contrário.
    """
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Lança exceção para erros HTTP

        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição para {url}: {e}")
        return None


def extract_data(json_response):
    """
    Extrai dados a partir da resposta JSON.
    Args:
        json_response (dict): Resposta JSON da qual os dados serão extraídos.
    Returns:
        dict or None: Dados extraídos se a estrutura for conforme esperado, None caso contrário.
    """
    if "dados" in json_response:
        return json_response["dados"]
    else:
        logger.warning("Estrutura de dados inesperada: %s", json_response)
        return None


def save_to_raw(data, file_path):
    """
    Salva dados em um arquivo bruto (formato JSON).

    Args:
        data (dict): Dados a serem salvos no arquivo.
        file_path (str): Caminho completo do arquivo onde os dados serão salvos.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Dados salvos em {file_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar dados em {file_path}: {e}")


def get_ids_deputados(file_path):
    """
    Obtém IDs de deputados a partir de um arquivo JSON.

    Args:
        file_path (str): Caminho do arquivo JSON contendo os dados dos deputados.

    Returns:
        list: Lista de IDs dos deputados.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        deputados = data.get("dados", [])
        ids = {deputado["id"] for deputado in deputados}
        logger.info(f"IDs dos deputados obtidos com sucesso do arquivo {file_path}")
        return ids
    except FileNotFoundError:
        logger.error(f"Arquivo {file_path} não encontrado.")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON em {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Erro inesperado ao obter IDs dos deputados de {file_path}: {e}")
        return []


def fetch_all_data(base_url, params=None):
    """
    Busca todos os dados através de respostas paginadas da API.

    Args:
        base_url (str): URL base da API para busca dos dados.
        params (dict, opcional): Parâmetros opcionais para a requisição GET. Default é None.

    Returns:
        list: Lista de todos os dados obtidos através de todas as respostas paginadas.
    """
    all_data = []
    url = base_url

    try:
        while url:
            data = fetch_data(url, params)
            if data:
                all_data.extend(data.get("dados", []))
                url = None
                for link in data.get("links", []):
                    if link.get("rel") == "next":
                        url = link.get("href")
                        break
                params = None
            else:
                break
    except Exception as e:
        logger.error(f"Erro ao buscar dados paginados em {url}: {e}")
        return []

    logger.info(f"Dados paginados obtidos com sucesso de {base_url}")
    return all_data
