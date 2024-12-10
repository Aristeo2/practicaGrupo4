# app/routers/mascotas.py
from fastapi import APIRouter, HTTPException, Depends
from app.services.mascotas_services import MascotasService

router = APIRouter()
mascotas_service = MascotasService()

@router.post("/")
def add_mascota(cliente_id: str, mascota: dict):
    return mascotas_service.add_mascota_to_cliente(cliente_id, mascota)

@router.get("/")
def get_mascotas(cliente_id: str):
    return mascotas_service.get_mascotas_by_cliente(cliente_id)

@router.get("/{mascota_id}")
def get_mascota(cliente_id: str, mascota_id: str):
    return mascotas_service.get_mascota_by_id(cliente_id, mascota_id)


@router.put("/{mascota_id}")
def update_mascota(cliente_id: str, mascota_id: str, mascota: dict):
    return mascotas_service.update_mascota(cliente_id, mascota_id, mascota)

@router.delete("/{mascota_id}")
def delete_mascota(cliente_id: str, mascota_id: str):
    return mascotas_service.delete_mascota(cliente_id, mascota_id)
