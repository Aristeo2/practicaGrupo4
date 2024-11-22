from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId


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
    id: Optional[PyObjectId] = Field(alias="_id")  # Se asigna automáticamente
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str  # ISO 8601 format (ej: "2023-11-10")
    patologias: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class Cliente(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")  # Se asigna automáticamente
    nombre: str
    dni: str
    direccion: str
    tlf: int
    email: str
    mascotas: List[Mascota] = []  # Mascotas embebidas

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}



