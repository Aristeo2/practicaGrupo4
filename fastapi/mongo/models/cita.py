from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import List, Optional
from .pyobjectid import PyObjectId  # Para manejar ObjectId en Pydantic

class Cita(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId)
    cliente_id: PyObjectId  # Relación con Cliente
    mascota_id: Optional[PyObjectId]  # Relación con Mascota
    fecha_inicio: datetime
    fecha_fin: datetime
    tratamiento: str
    subtratamientos: List[str] = []

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
