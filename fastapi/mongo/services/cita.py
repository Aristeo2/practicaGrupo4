from fastapi import HTTPException
from mongo.repositories.cita import CitaRepository
from mongo.models.cita import Cita
from mongo.models.citacreate import CitaCreateRequest
from datetime import datetime
from mongo.services.validarcita import ValidarCita



class CitasService:
    def __init__(self, cita_repo: CitaRepository, validar_cita: ValidarCita):
        self.cita_repo = cita_repo
        self.validar_cita = validar_cita

    def create_cita(self, cita_data: CitaCreateRequest):
        # Validate client existence
        cliente = self.validar_cita.validate_cliente(cita_data.cliente_id)

        # Validate pet existence and ownership
        mascota = self.validar_cita.validate_mascota(cita_data.mascota_id, cita_data.cliente_id)

        # Create the cita model
        nueva_cita = Cita(
            cliente_id=cita_data.cliente_id,
            mascota_id=cita_data.mascota_id,
            tratamiento=cita_data.tratamiento,
            sub_tratamientos=cita_data.sub_tratamientos,
            fecha_inicio=cita_data.fecha_inicio,
            fecha_fin=cita_data.fecha_fin,
            created_at=datetime.now(),
        )

        # Save the cita in the database
        self.cita_repo.save(nueva_cita)
        return nueva_cita

    def get_citas(self, cliente_id: str):
        # Validate client existence
        self.validar_cita.validate_cliente(cliente_id)
        return self.cita_repo.get_by_id(cliente_id)

    def eliminar_cita(self, cita_id: str):
        # Use cita_repo to delete
        deleted_count = self.cita_repo.delete(cita_id)
        if not deleted_count:
            raise ValueError("Cita no encontrada.")
        return deleted_count

    def obtener_todas_las_citas(self):
        # Use cita_repo to list all
        return self.cita_repo.list_all()

