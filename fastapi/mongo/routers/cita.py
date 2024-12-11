from fastapi import APIRouter, HTTPException
from mongo.services.cita import CitasService
from mongo.services.validarcita import ValidarCita
from mongo.repositories.cita import CitaRepository
from mongo.repositories.cliente import ClienteRepository
from mongo.repositories.mascotas import MascotaRepository
from mongo.models.citacreate import CitaCreateRequest
from mongo.db.database import citas_collection, mascotas_collection, clientes_collection

router = APIRouter()

validar_cita = ValidarCita(cliente_repo=MascotaRepository(mascotas_collection),mascota_repo=ClienteRepository(clientes_collection))
cita_service = CitasService(CitaRepository(citas_collection), validar_cita)


@router.post("/")
def create_cita(cita: CitaCreateRequest):
    """
    Crea una nueva cita.
    """
    try:
        # Save the cita and get its ID
        cita_id = cita_service.cita_repo.create(cita.dict())
        # Return the full cita data including the ID
        full_cita = {**cita.dict(), "id": cita_id}
        return full_cita
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{cita_id}")
def get_cita(cita_id: str):
    """
    Obtener una cita por su ID.
    """
    try:
        cita = cita_service.get_cita(cita_id)
        return cita
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{cita_id}")
def update_cita(cita_id: str, cita: dict):
    """
    Actualizar una cita por su ID.
    """
    updated_count = cita_service.cita_repo.update(cita_id, cita)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"message": "Cita actualizada"}

@router.delete("/{cita_id}")
def delete_cita(cita_id: str):
    try:
        deleted_count = cita_service.eliminar_cita(cita_id)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return {"message": "Cita eliminada"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all_citas():
    return cita_service.obtener_todas_las_citas()
