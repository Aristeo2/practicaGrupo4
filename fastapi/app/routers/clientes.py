# app/routers/clientes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.schemas import Cliente
from app.services.clientes_services import ClienteService

router = APIRouter()

# Servicio de clientes
cliente_service = ClienteService()

@router.post("/clientes/", response_model=Cliente)
def create_cliente(cliente: Cliente):
    return cliente_service.create_cliente(cliente)

@router.get("/clientes/", response_model=List[Cliente])
def get_all_clientes():
    return cliente_service.get_all_clientes()

@router.get("/clientes/{cliente_id}", response_model=Cliente)
def get_cliente(cliente_id: str):
    cliente = cliente_service.get_cliente_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/clientes/{cliente_id}", response_model=Cliente)
def update_cliente(cliente_id: str, cliente: Cliente):
    updated_cliente = cliente_service.update_cliente(cliente_id, cliente)
    if not updated_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return updated_cliente

@router.delete("/clientes/{cliente_id}")
def delete_cliente(cliente_id: str):
    if not cliente_service.delete_cliente(cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado correctamente"}
