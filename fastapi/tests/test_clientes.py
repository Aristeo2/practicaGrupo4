from fastapi.testclient import TestClient
from app.main import app
from app.schemas.schemas import Cliente
from app.services.clientes_services import ClienteService
import pytest 

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API SOLID"}

def test_get_all_clientes():
    response = client.get("/api/clientes")
    assert response.status_code == 200
    # Asegúrate de que retorna una lista
    assert isinstance(response.json(), list)

def test_create_cliente():
    nuevo_cliente = {
        "nombre": "Prueba Cliente",
        "dni": "12345678P",
        "direccion": "Calle Prueba, 123",
        "tlf": 123456789,
        "email": "prueba@correo.com",
        "mascotas": []
    }
    response = client.post("/api/clientes/", json=nuevo_cliente)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Prueba Cliente"
    assert data["dni"] == "12345678P"
    



@pytest.fixture
def cliente_service(mocker):
    # Crea una instancia de ClienteService
    service = ClienteService()
    # Si es necesario, puedes agregar mocks a sus métodos
    mocker.patch.object(service.db, "find_one")
    mocker.patch.object(service.db, "update_one")
    mocker.patch.object(service.db, "delete_one")
    return service


def test_get_cliente_by_id(cliente_service, mocker):
    # Mock de los datos de un cliente
    mock_cliente = {
        "_id": "test_id",
        "nombre": "Prueba Cliente",
        "dni": "12345678P",
        "direccion": "Calle Prueba, 123",
        "tlf": 123456789,
        "email": "prueba@correo.com",
        "mascotas": []
    }
    # Mock del método find_one de la base de datos
    mocker.patch.object(cliente_service.db, "find_one", return_value=mock_cliente)
    
    # Llamar a la función
    result = cliente_service.get_cliente_by_id("test_id")
    
    assert result is not None
    assert result.nombre == "Prueba Cliente"
    assert result.dni == "12345678P"

def test_update_cliente(cliente_service, mocker):
    # Mock de los datos originales y actualizados de un cliente
    mock_cliente_original = {
        "_id": "test_id",
        "nombre": "Cliente Original",
        "dni": "12345678O",
        "direccion": "Calle Original, 123",
        "tlf": 987654321,
        "email": "original@correo.com",
        "mascotas": []
    }
    mock_cliente_actualizado = {
        "_id": "test_id",
        "nombre": "Cliente Actualizado",
        "dni": "12345678A",
        "direccion": "Calle Actualizada, 456",
        "tlf": 123456789,
        "email": "actualizado@correo.com",
        "mascotas": []
    }
    
    # Mock del método update_one y find_one de la base de datos
    mocker.patch.object(cliente_service.db, "update_one", return_value=mocker.Mock(modified_count=1))
    mocker.patch.object(cliente_service.db, "find_one", return_value=mock_cliente_actualizado)
    
    # Crear el objeto Cliente actualizado
    cliente_actualizado = Cliente(**mock_cliente_actualizado)
    
    # Llamar a la función
    result = cliente_service.update_cliente("test_id", cliente_actualizado)
    
    assert result is not None
    assert result.nombre == "Cliente Actualizado"
    assert result.dni == "12345678A"

def test_delete_cliente(cliente_service, mocker):
    # Mock del método delete_one de la base de datos
    mocker.patch.object(cliente_service.db, "delete_one", return_value=mocker.Mock(deleted_count=1))
    
    # Llamar a la función
    result = cliente_service.delete_cliente("test_id")
    
    assert result is True
