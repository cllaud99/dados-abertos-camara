from get_api_data import fetch_all_data, fetch_data, get_ids_deputados, save_to_raw
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


def save_json_to_db():
    """
    Função que itera sobre arquivos de uma pasta, valida com pydantic e caso esteja O.K. salva em um banco postgresql
    """
    pass


if __name__ == "__main__":
    download_data()
