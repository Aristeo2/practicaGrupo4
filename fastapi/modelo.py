#Base model template
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class Cliente(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    dni: str
    direccion: str
    tlf: int
    email:str

class Mascota(BaseModel):
    id: str  = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre:str
    especie:str
    raza: str
    fecha_nacimiento: datetime
    patologias: str
    dueño: str