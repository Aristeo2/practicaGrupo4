from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.clientes import Cliente, ClienteCreate
from app.services.clientes_service import ClientesService

router = APIRouter()

@router.get("/clientes", response_model=List[Cliente])
def get_all_clientes(clientes_service: ClientesService = Depends()):
    return clientes_service.get_all_clientes()

@router.get("/clientes/{cliente_id}", response_model=Cliente)
def get_cliente(cliente_id: str, clientes_service: ClientesService = Depends()):
    cliente = clientes_service.get_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/clientes", response_model=Cliente)
def create_cliente(cliente: ClienteCreate, clientes_service: ClientesService = Depends()):
    return clientes_service.create_cliente(cliente)
