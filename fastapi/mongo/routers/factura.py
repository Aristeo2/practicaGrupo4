from fastapi import APIRouter, HTTPException
from mongo.services import FacturaService
from mongo.repositories import FacturaRepository
from mongo.repositories import CitaRepository
from mongo.db.database import facturas_collection, citas_collection
from mongo.models.facturacreate import FacturaCreateRequest

router = APIRouter()
factura_service = FacturaService(
    FacturaRepository(facturas_collection),
    CitaRepository(citas_collection)
)

@router.post("/")
def create_factura(factura_data: FacturaCreateRequest):
    try:
        factura_id = factura_service.generar_factura(factura_data.cita_id, factura_data.precio)
        return {"id": factura_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all_facturas():
    """
    Obtener todas las facturas.
    """
    facturas = factura_service.factura_repo.list_all()
    return facturas