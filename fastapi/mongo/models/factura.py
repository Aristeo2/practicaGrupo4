from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Optional
from .pyobjectid import PyObjectId  # Para manejar ObjectId en Pydantic

class Factura(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId)
    id_cita: PyObjectId  # Relación con Cita
    id_cliente: PyObjectId  # Relación con Cliente
    id_mascota: PyObjectId  # Relación con Mascota
    tratamiento: str  # Nombre del tratamiento (de la cita)
    fecha_cita: datetime  # Fecha de la cita
    precio: float  # Precio total de la factura

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
