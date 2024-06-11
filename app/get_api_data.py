import requests
import duckdb
import os
import json

def fetch_data(url, params=None):
    """Fetch data from the given URL with headers and optional parameters."""
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None

def extract_data(json_response):
    """Extract data from the JSON response."""
    if 'dados' in json_response:
        return json_response['dados']
    else:
        print("Estrutura de dados inesperada:", json_response)
        return None

def save_to_raw(data, file_path):
    """Save data to a raw file (JSON format)."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_ids_deputados(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    deputados = data.get('dados', [])
    ids = [deputado['id'] for deputado in deputados]
    return ids


def fetch_all_data(base_url, params=None):
    """Fetch all data across paginated API responses."""
    all_data = []
    url = base_url
    
    while url:
        data = fetch_data(url, params)
        if data:
            all_data.extend(data['dados'])
            url = None
            for link in data['links']:
                if link['rel'] == 'next':
                    url = link['href']
                    break
            # Reset params after the first request to follow the next URLs directly
            params = None
        else:
            break
    
    return all_data
