from mongo.repositories.cliente import ClienteRepository
from mongo.repositories.mascotas import MascotaRepository
from fastapi import HTTPException

class ValidarCita:
    def __init__(self, cliente_repo: ClienteRepository, mascota_repo: MascotaRepository):
        self.cliente_repo = cliente_repo
        self.mascota_repo = mascota_repo

    def validate_cliente(self, cliente_id: str):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente

    def validate_mascota(self, mascota_id: str, cliente_id: str):
        mascota = self.mascota_repo.get_by_id(mascota_id)
        if not mascota:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        if str(mascota["cliente_id"]) != cliente_id:
            raise HTTPException(status_code=400, detail="La mascota no pertenece al cliente especificado")
        return mascota
