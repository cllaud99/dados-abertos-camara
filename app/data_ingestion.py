from get_api_data import fetch_all_data, fetch_data, get_ids_deputados, save_to_raw
from landing_zone_data_processing import read_and_validate_json, read_normalize_json
from db_operations import insert_data_to_postgres, build_external_database_url, validate_postgresql_connection
from models import Despesa
from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
from tqdm import tqdm


def download_data():
    """
    Função que realiza o download de arquivos JSON e armazena em uma landing_zone
    """
    path_deputados_file = "data/landing_zone/deputados_raw.json"
    deputados = fetch_data("https://dadosabertos.camara.leg.br/api/v2/deputados")
    save_to_raw(deputados, path_deputados_file)

    ids = get_ids_deputados(path_deputados_file)
    print(ids)

    for id in tqdm(ids):

        url_infos = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id}"
        data_infos = fetch_data(url_infos)
        file_path_infos = f"data/landing_zone/infos/{id}_infos.json"
        save_to_raw(data_infos, file_path_infos)

        url_despesas = (
            f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/despesas"
        )
        params_despesas = {"ano": "2024"}
        data_despesas = fetch_all_data(url_despesas, params=params_despesas)
        file_path_despesas = f"data/landing_zone/despesas/{id}_despesas.json"
        save_to_raw(data_despesas, file_path_despesas)


def normalize_and_save(folder_path, model, table_name):
    json_folder = Path(folder_path)
    external_database_url = build_external_database_url()
    engine = create_engine(external_database_url)
    if validate_postgresql_connection(engine):
        for file_path in json_folder.glob("*.json"):
            try:
                validated_items = read_and_validate_json(file_path, model)
                if validated_items:
                    df = pd.DataFrame([item.model_dump() for item in validated_items])
                    print(f"Dados válidos no arquivo {file_path}:")
                    
                    insert_data_to_postgres(df, table_name, engine)
                    
                    print(f"Dados do arquivo {file_path} foram inseridos com sucesso na tabela 'raw_despesas'.")
                else:
                    print(f"Dados inválidos no arquivo {file_path}")
            except Exception as e:
                print(f"Ocorreu um erro ao processar o arquivo {file_path}: {e}")


if __name__ == "__main__":
    folder_path = "data/landing_zone/despesas"
    table_name = 'raw_despesas'
    model = Despesa
    normalize_and_save(folder_path, table_name, model)
