import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def create_test_cliente():
    cliente_data = {
        "nombre": "Test Cliente",
        "dni": "12345678A",
        "direccion": "Calle Falsa 123",
        "tlf": 987654321,
        "email": "test@example.com"
    }
    response = client.post("/clientes/", json=cliente_data)
    assert response.status_code == 200
    return response.json()["id"]

@pytest.fixture
def create_test_mascota(create_test_cliente):
    mascota_data = {
        "id_cliente": create_test_cliente,
        "nombre": "Firulais",
        "especie": "Perro",
        "raza": "Labrador",
        "fecha_nacimiento": "2020-05-10",
        "patologias": "Alergia"
    }
    response = client.post("/mascotas/", json=mascota_data)
    assert response.status_code == 200
    return response.json()["id"]

@pytest.fixture
def create_test_cita(create_test_cliente, create_test_mascota):
    cita_data = {
        "fecha_inicio": "2024-12-15T09:00:00",
        "fecha_fin": "2024-12-15T10:00:00",
        "tratamiento": "Control veterinario",
        "sub_treatments": ["Vacunación", "Desparasitación"],
        "cliente_id": create_test_cliente,
        "mascota_id": create_test_mascota
    }
    response = client.post("/citas/", json=cita_data)
    assert response.status_code == 200
    return response.json()["id"]

def test_create_factura(create_test_cita):
    factura_data = {
        "cita_id": create_test_cita,
        "precio": 100.50
    }
    response = client.post("/facturas/", json=factura_data)
    assert response.status_code == 200
    assert "id" in response.json()

def test_list_all_facturas():
    response = client.get("/facturas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
