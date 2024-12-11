from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from .pyobjectid import PyObjectId  # Para manejar ObjectId en Pydantic

class Mascota(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId)
    id_cliente: PyObjectId  # Relación con Cliente
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str  # ISO 8601 format (ej: "2023-11-10")
    patologias: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
