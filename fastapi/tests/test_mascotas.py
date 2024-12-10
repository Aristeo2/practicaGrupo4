import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.mascotas_services import MascotasService
from bson import ObjectId

client = TestClient(app)


@pytest.fixture
def mock_database(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch("app.services.mascotas_services.Database.get_collection", return_value=mock_db)
    return mock_db


@pytest.fixture
def mascota_service(mock_database):
    return MascotasService()


def test_get_all_mascotas(mock_database):
    cliente_id = str(ObjectId())  # Genera un ObjectId válido
    mock_database.find_one.return_value = {
        "_id": cliente_id,
        "mascotas": [
            {"nombre": "Firulais", "especie": "Perro", "raza": "Labrador", "fecha_nacimiento": "2020-01-01"}
        ]
    }
    response = client.get(f"/clientes/{cliente_id}/mascotas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["nombre"] == "Firulais"

def test_create_mascota(mock_database):
    cliente_id = str(ObjectId())  # Genera un ObjectId válido
    nueva_mascota = {
        "nombre": "Firulais",
        "especie": "Perro",
        "raza": "Labrador",
        "fecha_nacimiento": "2020-01-01"
    }
    mock_database.update_one.return_value = None
    response = client.post(f"/clientes/{cliente_id}/mascotas", json=nueva_mascota)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Firulais"
    assert data["especie"] == "Perro"
    assert data["fecha_nacimiento"] == "2020-01-01"

def test_get_mascota_by_id(mock_database):
    cliente_id = str(ObjectId())  # Genera un ObjectId válido
    mascota_id = str(ObjectId())  # Genera un ObjectId válido
    mock_database.find_one.return_value = {
        "_id": cliente_id,
        "mascotas": [
            {"_id": mascota_id, "nombre": "Firulais", "especie": "Perro", "raza": "Labrador", "fecha_nacimiento": "2020-01-01"}
        ]
    }
    response = client.get(f"/clientes/{cliente_id}/mascotas/{mascota_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Firulais"
    assert data["especie"] == "Perro"
    assert data["fecha_nacimiento"] == "2020-01-01"
