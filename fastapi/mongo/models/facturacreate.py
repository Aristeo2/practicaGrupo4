from pydantic import BaseModel

class FacturaCreateRequest(BaseModel):
    cita_id: str
    precio: float
