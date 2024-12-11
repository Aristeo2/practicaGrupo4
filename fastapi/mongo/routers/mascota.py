from fastapi import APIRouter, HTTPException
from mongo.repositories import MascotaRepository
from mongo.db.database import mascotas_collection

router = APIRouter()
mascota_repo = MascotaRepository(mascotas_collection)

@router.post("/")
def create_mascota(mascota: dict):
    mascota_id = mascota_repo.create(mascota)
    return {"id": mascota_id}

@router.get("/{mascota_id}")
def get_mascota(mascota_id: str):
    mascota = mascota_repo.get_by_id(mascota_id)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

@router.put("/{mascota_id}")
def update_mascota(mascota_id: str, mascota: dict):
    """
    Actualizar una mascota por su ID.
    """
    updated_count = mascota_repo.update(mascota_id, mascota)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return {"message": "Mascota actualizada"}

@router.delete("/{mascota_id}")
def delete_mascota(mascota_id: str):
    """
    Eliminar una mascota por su ID.
    """
    deleted_count = mascota_repo.delete(mascota_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return {"message": "Mascota eliminada"}

@router.get("/")
def get_all_mascotas():
    """
    Obtener todas las mascotas.
    """
    mascotas = mascota_repo.list_all()
    return mascotas