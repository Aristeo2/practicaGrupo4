from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from .pyobjectid import PyObjectId  # Para manejar ObjectId en Pydantic

class Cliente(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId)
    nombre: str
    dni: str
    direccion: str
    tlf: int
    email: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
