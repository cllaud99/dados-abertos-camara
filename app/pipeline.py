import json
from get_api_data import fetch_data, extract_data, save_to_raw
from tqdm import tqdm

endpoint = 'deputados'

def get_deputados():
    url = f'https://dadosabertos.camara.leg.br/api/v2/{endpoint}'
    
    raw_file_path = f'data/bronze/{endpoint}_raw.json'
    
    response = fetch_data(url)
    if response:
        data = extract_data(response)
        if data:
            save_to_raw(data, raw_file_path)

def get_ids_deputados(file_path):

    with open(file_path, 'r') as file:
        deputados = json.load(file)
    ids = [deputado['id'] for deputado in deputados]
    print(ids)
    return ids

def get_all_dep_infos():

    ids = get_ids_deputados()

    endpoints = [
    "",    
    "/despesas",
    "/discursos",
    "/eventos",
    "/frentes",
    "/historico",
    "/mandatosExternos",
    "/ocupacoes",
    "/orgaos",
    "/profissoes"
    ]
    
    total_iterations = len(ids) * len(endpoints)

    with tqdm(total=total_iterations, desc="Progresso") as pbar:
        for id in ids:

            headers = {'Accept': 'application/json'}

            for endpoint in endpoints:

                url = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}{endpoint}'

                raw_file_path = f'data/bronze/{endpoint}_{id}_raw.json'

                response = fetch_data(url)

                if response:

                    data = extract_data(response)

                    if data:
                        save_to_raw(data, raw_file_path)
                
                pbar.update(1) 

get_deputados()
get_all_dep_infos()