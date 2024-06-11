from get_api_data import fetch_data, save_to_raw, get_ids_deputados, fetch_all_data
from tqdm import tqdm

path_deputados_file = 'data/bronze/deputados_raw.json'
deputados = fetch_data('https://dadosabertos.camara.leg.br/api/v2/deputados')
save_to_raw(deputados, path_deputados_file)


path_votacoes_file = 'data/bronze/votacoes_raw.json'
params_votacoes = {'dataInicio': '2022-01-01', 'dataFim': '2025-01-01'}
votacoes = fetch_all_data('https://dadosabertos.camara.leg.br/api/v2/votacoes')
save_to_raw(votacoes, path_votacoes_file)


ids = get_ids_deputados(path_deputados_file)
print(ids)

for id in tqdm(ids):

    url_infos = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}'
    data_infos = fetch_data(url_infos)
    file_path_infos = f'data/bronze/infos/{id}_infos.json'
    save_to_raw(data_infos, file_path_infos)

    url_despesas = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/despesas'
    params_despesas = {'ano': '2022,2023,2024'}
    data_despesas = fetch_all_data(url_despesas, params=params_despesas)
    file_path_despesas = f'data/bronze/despesas/{id}_despesas.json'
    save_to_raw(data_despesas, file_path_despesas)

    url_discursos = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/discursos'
    params_discursos = {'dataInicio': '2022-01-01', 'dataFim': '2025-01-01'}
    data_discursos = fetch_all_data(url_discursos, params=params_discursos)
    file_path_discursos = f'data/bronze/discursos/{id}_discursos.json'
    save_to_raw(data_discursos, file_path_discursos)
