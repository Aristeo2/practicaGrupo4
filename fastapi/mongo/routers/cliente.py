from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from mongo.services import ClienteService
from mongo.repositories import ClienteRepository
from mongo.repositories import MascotaRepository
from mongo.models.cliente import Cliente
from mongo.db.database import clientes_collection, mascotas_collection

router = APIRouter()
cliente_service = ClienteService(
    ClienteRepository(clientes_collection),
    MascotaRepository(mascotas_collection)
)

@router.post("/")
def create_cliente(cliente: dict):
    try:
        cliente_id = cliente_service.cliente_repo.create(cliente)
        return {"id": cliente_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: str):
    try:
        cliente_service.eliminar_cliente(cliente_id)
        return {"message": "Cliente y sus mascotas eliminados"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{cliente_id}", response_model=Cliente)
def get_cliente(cliente_id: str):
    try:
        cliente = cliente_service.get_cliente(cliente_id)
        return cliente
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{cliente_id}")
def update_cliente(cliente_id: str, cliente: dict):
    """
    Actualizar un cliente por su ID.
    """
    updated_count = cliente_service.cliente_repo.update(cliente_id, cliente)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente actualizado"}

@router.get("/")
def get_all_clientes():
    """
    Obtener todos los clientes.
    """
    clientes = cliente_service.cliente_repo.list_all()
    return clientes
