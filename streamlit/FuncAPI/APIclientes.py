
import requests

API_URL = "http://fastapi:8000"

def get_clientes():
    response = requests.get(f"{API_URL}/clientes/")
    if response.status_code == 200:
        clientes = response.json()
        return clientes
    return []

def create_cliente(cliente):
    cliente.pop("id", None)  # Elimina el campo `id` si ya existe
    response = requests.post(f"{API_URL}/clientes/", json=cliente)
    return response.json() if response.status_code == 200 else None
