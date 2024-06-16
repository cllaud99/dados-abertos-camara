import json
import os

import duckdb
import requests


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
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.status_code}")
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
        print("Estrutura de dados inesperada:", json_response)
        return None


def save_to_raw(data, file_path):
    """
    Salva dados em um arquivo bruto (formato JSON).

    Args:
        data (dict): Dados a serem salvos no arquivo.
        file_path (str): Caminho completo do arquivo onde os dados serão salvos.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_ids_deputados(file_path):
    """
    Obtém IDs de deputados a partir de um arquivo JSON.

    Args:
        file_path (str): Caminho do arquivo JSON contendo os dados dos deputados.

    Returns:
        list: Lista de IDs dos deputados.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    deputados = data.get("dados", [])
    ids = [deputado["id"] for deputado in deputados]
    return ids


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

    while url:
        data = fetch_data(url, params)
        if data:
            all_data.extend(data["dados"])
            url = None
            for link in data["links"]:
                if link["rel"] == "next":
                    url = link["href"]
                    break
            params = None
        else:
            break

    return all_data
