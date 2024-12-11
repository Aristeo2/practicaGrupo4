import pytest
from fastapi.testclient import TestClient
from main import app  # Asegúrate de importar la aplicación principal FastAPI

client = TestClient(app)

@pytest.fixture
def mascota_data():
    return {
        "id_cliente": "64d4f03db9b3e89fb3c4e741",  # Cambia por un ID válido de cliente
        "nombre": "Firulais",
        "especie": "Perro",
        "raza": "Labrador",
        "fecha_nacimiento": "2021-05-10",
        "patologias": "Ninguna"
    }

def test_create_mascota(mascota_data):
    response = client.post("/mascotas/", json=mascota_data)
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_mascota(mascota_data):
    create_response = client.post("/mascotas/", json=mascota_data)
    mascota_id = create_response.json()["id"]

    response = client.get(f"/mascotas/{mascota_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == mascota_data["nombre"]

def test_update_mascota(mascota_data):
    create_response = client.post("/mascotas/", json=mascota_data)
    mascota_id = create_response.json()["id"]

    updated_data = {**mascota_data, "nombre": "Firu actualizado"}
    response = client.put(f"/mascotas/{mascota_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Mascota actualizada"

def test_delete_mascota(mascota_data):
    create_response = client.post("/mascotas/", json=mascota_data)
    mascota_id = create_response.json()["id"]

    response = client.delete(f"/mascotas/{mascota_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Mascota eliminada"

def test_get_all_mascotas(mascota_data):
    client.post("/mascotas/", json=mascota_data)

    response = client.get("/mascotas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
