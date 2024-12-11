import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Template para datos de prueba
cita_data_template = {
    "fecha_inicio": "2024-12-15T09:00:00",
    "fecha_fin": "2024-12-15T10:00:00",
    "tratamiento": "Control veterinario",
    "sub_treatments": ["Vacunación", "Desparasitación"]
}

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

def test_create_cita(create_test_cliente, create_test_mascota):
    cita_data = cita_data_template.copy()
    cita_data["cliente_id"] = create_test_cliente
    cita_data["mascota_id"] = create_test_mascota

    response = client.post("/citas/", json=cita_data)
    assert response.status_code == 200
    assert response.json()["cliente_id"] == create_test_cliente
    assert response.json()["mascota_id"] == create_test_mascota

def test_update_cita(create_test_cliente, create_test_mascota):
    cita_data = cita_data_template.copy()
    cita_data["cliente_id"] = create_test_cliente
    cita_data["mascota_id"] = create_test_mascota

    create_response = client.post("/citas/", json=cita_data)
    assert create_response.status_code == 200
    cita_id = create_response.json()["id"]

    update_data = {
        "fecha_inicio": "2024-12-15T11:00:00",
        "fecha_fin": "2024-12-15T12:00:00",
        "tratamiento": "Consulta general",
        "sub_treatments": ["Revisión general"]
    }

    update_response = client.put(f"/citas/{cita_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Cita actualizada"

def test_delete_cita(create_test_cliente, create_test_mascota):
    cita_data = cita_data_template.copy()
    cita_data["cliente_id"] = create_test_cliente
    cita_data["mascota_id"] = create_test_mascota

    create_response = client.post("/citas/", json=cita_data)
    assert create_response.status_code == 200
    cita_id = create_response.json()["id"]

    delete_response = client.delete(f"/citas/{cita_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Cita eliminada"

def test_get_all_citas():
    response = client.get("/citas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

