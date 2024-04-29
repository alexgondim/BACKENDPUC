import requests

def get_address_by_cep(cep: str):
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    return response.json() if response.status_code == 200 else None
