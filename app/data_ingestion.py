import os
from pathlib import Path

from dotenv import load_dotenv
import pandas as pd
import json
from db_operations import (
    build_external_database_url,
    create_postgres_schema,
    drop_all_tables_in_schema,
    insert_data_to_postgres,
    validate_postgresql_connection,
)
from get_api_data import fetch_all_data, fetch_data, get_ids_deputados, save_to_raw
from landing_zone_data_processing import read_and_validate_json, normalize_columns_with_json
from models import DadosDeputado, Deputado, Despesa, DeputadoHistorico
from sqlalchemy import create_engine
from tqdm import tqdm


load_dotenv()

sample_run = os.getenv('SAMPLE_RUN')
print(sample_run)
ID_LEGISLATURA = 57

external_database_url = build_external_database_url()
engine = create_engine(external_database_url)


def download_data():
    """
    Função que realiza o download de arquivos JSON e armazena em uma landing_zone
    """
    path_deputados_file = "data/landing_zone/deputados_raw.json"
    deputados = fetch_data("https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=57")
    save_to_raw(deputados, path_deputados_file)

    ids = get_ids_deputados(path_deputados_file)
    if sample_run != "False":

        ids = ids[:5]
    print(ids)

    for id in tqdm(ids):

        url_infos = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id}"
        data_infos = fetch_data(url_infos)
        file_path_infos = f"data/landing_zone/infos/{id}_infos.json"
        save_to_raw(data_infos, file_path_infos)

        url_despesas = (
            f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/despesas"
        )
        params_despesas = {"idLegislatura": ID_LEGISLATURA}
        data_despesas = fetch_all_data(url_despesas, params=params_despesas)
        file_path_despesas = f"data/landing_zone/despesas/{id}_despesas.json"
        save_to_raw(data_despesas, file_path_despesas)

        url_historico = (
            f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/historico"
        )
        data_historico = fetch_all_data(url_historico)
        file_path_historico = f"data/landing_zone/historico/{id}_historico.json"
        save_to_raw(data_historico, file_path_historico)


def normalize_and_save(json_folder, model, table_name, engine):
    if validate_postgresql_connection(engine):
        for file_path in tqdm(list(json_folder.glob("*.json"))):  # Usar tqdm na lista de arquivos
            try:
                validated_items = read_and_validate_json(file_path, model)
                if validated_items:
                    data_to_insert = []
                    print(f"Dados válidos no arquivo {file_path}:")

                    for item in validated_items:
                        # Serializar UltimoStatus para JSON
                        item_dict = item.model_dump()
                        if 'ultimoStatus' in item_dict and item_dict['ultimoStatus'] is not None:
                            item_dict['ultimoStatus'] = json.dumps(item_dict['ultimoStatus'])

                        item_dict['file_name'] = Path(file_path).name
                        data_to_insert.append(item_dict)

                    df = pd.DataFrame(data_to_insert)

                    insert_data_to_postgres(df, table_name, engine)
                    print(f"Dados do arquivo {file_path} foram inseridos com sucesso na tabela {table_name}.")

                else:
                    print(f"Nenhum dado válido no arquivo {file_path}.")
                    
            except Exception as e:
                print(f"Ocorreu um erro ao processar o arquivo {file_path}: {e}")


if __name__ == "__main__":
    download_data()
    create_postgres_schema(engine, 'public')
    drop_all_tables_in_schema(engine, "public")
    normalize_and_save(Path("data/landing_zone/"), Deputado, "lz_deputados", engine)
    normalize_and_save(Path("data/landing_zone/despesas"), Despesa, "lz_despesas", engine)
    normalize_and_save(Path("data/landing_zone/infos"), DadosDeputado, "lz_infos_extras", engine)
    normalize_and_save(Path("data/landing_zone/historico"), DeputadoHistorico, "lz_historico_deputado", engine)