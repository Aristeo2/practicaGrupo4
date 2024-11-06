#Base model template
from typing import Optional
from pydantic import BaseModel, Field
import datetime
import uuid

class Cliente(BaseModel):
    id: str
    nombre: str
    dni: str
    direccion: str
    tlf: int
    email:str

class Mascota(BaseModel):
    id: str
    nombre:str
    especie:str
    raza: str
    fecha_nacimiento: datetime
    patologias: str
    dueño: str