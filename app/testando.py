import json

from models import DadosDeputado
from pydantic import ValidationError

# Dados de exemplo
file_path = "data/landing_zone/infos/62881_infos.json"

try:
    with open(file_path, "r", encoding="utf-8") as file:
        dados_json = json.load(file)

        # Criando uma instância de DadosDeputado e validando
        dados_deputado = DadosDeputado(**dados_json)
        print("Dados válidos:")
        print(dados_deputado)

except FileNotFoundError:
    print(f"Arquivo '{file_path}' não encontrado.")
except json.JSONDecodeError as e:
    print(f"Erro ao decodificar JSON: {e}")
except ValidationError as e:
    print("Erro de validação:")
    print(e.json())
