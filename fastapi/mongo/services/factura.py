from mongo.repositories import FacturaRepository
from mongo.repositories import CitaRepository

class FacturaService:
    def __init__(self, factura_repo: FacturaRepository, cita_repo: CitaRepository):
        self.factura_repo = factura_repo
        self.cita_repo = cita_repo

    def generar_factura(self, cita_id: str, precio: float):
        """
        Genera una factura basada en una cita.
        :param cita_id: ID de la cita asociada.
        :param precio: Precio total de la factura.
        :return: ID de la factura creada.
        """
        # Obtener la cita desde el repositorio
        cita = self.cita_repo.get_by_id(cita_id)
        if not cita:
            raise ValueError("Cita no encontrada")

        # Validar que la cita tiene información necesaria
        if not cita.get("cliente_id") or not cita.get("mascota_id"):
            raise ValueError("La cita no tiene cliente o mascota asociados")

        # Crear el documento de factura
        factura = {
            "id_cita": cita_id,
            "id_cliente": cita["cliente_id"],
            "id_mascota": cita["mascota_id"],
            "tratamiento": cita["tratamiento"],
            "fecha_cita": cita["fecha_inicio"],
            "precio": precio,
        }

        # Guardar la factura en la base de datos
        return self.factura_repo.create(factura)
