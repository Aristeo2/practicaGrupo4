import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Datos de ejemplo para los tests
cliente_data = {
    "nombre": "Cliente Test",
    "dni": "12345678",
    "direccion": "Dirección 1",
    "tlf": 123456789,
    "email": "cliente@example.com"
}

@pytest.fixture
def create_test_cliente():
    """
    Crea un cliente de prueba antes de cada test.
    """
    response = client.post("/clientes/", json=cliente_data)
    assert response.status_code == 200
    return response.json()["id"]

def test_create_cliente():
    """
    Test para crear un cliente.
    """
    response = client.post("/clientes/", json=cliente_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"]

def test_get_cliente(create_test_cliente):
    """
    Test para obtener un cliente por su ID.
    """
    cliente_id = create_test_cliente
    response = client.get(f"/clientes/{cliente_id}")
    assert response.status_code == 200
    cliente = response.json()
    assert cliente["nombre"] == cliente_data["nombre"]

def test_update_cliente(create_test_cliente):
    """
    Test para actualizar un cliente.
    """
    cliente_id = create_test_cliente
    update_data = {"nombre": "Cliente Actualizado"}
    response = client.put(f"/clientes/{cliente_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Cliente actualizado"

    # Verificar la actualización
    response = client.get(f"/clientes/{cliente_id}")
    assert response.status_code == 200
    cliente = response.json()
    assert cliente["nombre"] == "Cliente Actualizado"

def test_delete_cliente(create_test_cliente):
    """
    Test para eliminar un cliente.
    """
    cliente_id = create_test_cliente
    response = client.delete(f"/clientes/{cliente_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Cliente y sus mascotas eliminados"

    # Verificar que el cliente no existe
    response = client.get(f"/clientes/{cliente_id}")
    assert response.status_code == 404

def test_get_all_clientes(create_test_cliente):
    """
    Test para obtener todos los clientes.
    """
    response = client.get("/clientes/")
    assert response.status_code == 200
    clientes = response.json()
    assert isinstance(clientes, list)
    assert any(cliente["nombre"] == cliente_data["nombre"] for cliente in clientes)

