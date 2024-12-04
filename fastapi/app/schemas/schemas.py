from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
import uuid


# Manejo de ObjectId como cadena en Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Mascota(BaseModel):
    id: Optional[str]  
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str  # ISO 8601 format (ej: "2023-11-10")
    patologias: Optional[str] = None



class Cliente(BaseModel):
    id: Optional[str] = None
    nombre: str
    dni: str
    direccion: str
    tlf: int
    email: str
    mascotas: List[Mascota] = []  # Mascotas embebidas

    class Config:
        json_encoders = {uuid.UUID: str}  # Convierte UUID a string si es necesario



class Cita(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    cliente_id: str  # Relación con Cliente
    mascota_id: Optional[str]  # Relación con Mascota
    fecha_inicio: datetime
    fecha_fin: datetime
    tratamiento: str
    subtratamientos: List[str] = []

    class Config:
        json_encoders = {uuid.UUID: str}