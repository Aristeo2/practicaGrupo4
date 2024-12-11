from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CitaCreateRequest(BaseModel):
    cliente_id: str = Field(..., description="ID del cliente asociado a la cita")
    mascota_id: str = Field(..., description="ID de la mascota asociada a la cita")
    tratamiento: str = Field(..., description="Tratamiento principal a realizar en la cita")
    fecha_inicio: datetime = Field(..., description="Fecha y hora de inicio de la cita")
    fecha_fin: datetime = Field(..., description="Fecha y hora de finalización de la cita")
    subtratamientos: Optional[List[str]] = Field(default=[], description="Lista de subtratamientos opcionales para la cita")

    class Config:
        schema_extra = {
            "example": {
                "cliente_id": "123abc",
                "mascota_id": "456def",
                "tratamiento": "Consulta general",
                "fecha_inicio": "2024-12-15T09:00:00",
                "fecha_fin": "2024-12-15T10:00:00",
                "subtratamientos": ["Vacunación", "Limpieza dental"]
            }
        }
