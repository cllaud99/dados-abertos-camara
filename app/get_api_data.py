import requests
import duckdb
import pandas as pd

def fetch_data(url, headers):
    """Fetch data from the given URL with headers."""
    response = requests.get(url, headers=headers)
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

def save_to_duckdb(data, table ,db_path='dados-abertos-camara.duckdb'):
    """Save the data to a DuckDB database."""
    df = pd.DataFrame(data)
    conn = duckdb.connect(db_path)
    conn.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM df")
    conn.close()

def main():
    url = 'https://dadosabertos.camara.leg.br/api/v2/blocos'
    headers = {'Accept': 'application/json'}
    
    response = fetch_data(url, headers)
    if response:
        data = extract_data(response)
        if data:
            save_to_duckdb(data, 'blocos')

if __name__ == "__main__":
    main()
