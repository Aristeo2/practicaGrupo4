import requests

API_URL = "http://127.0.0.1:8000"  # URL de la API de FastAPI


# Funciones auxiliares para consumir la API

class API_CLiente:
    @staticmethod
    def get_clientes():
        response = requests.get(f"{API_URL}/clientes/")
        return response.json() if response.status_code == 200 else []
    @staticmethod
    def create_cliente(cliente):
        response = requests.post(f"{API_URL}/clientes/", json=cliente)
        return response.json() if response.status_code == 200 else None

def get_mascotas():
    response = requests.get(f"{API_URL}/mascotas/")
    return response.json() if response.status_code == 200 else []

def create_mascota(mascota):
    response = requests.post(f"{API_URL}/mascotas/", json=mascota)
    return response.json() if response.status_code == 200 else None