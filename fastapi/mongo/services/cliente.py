from mongo.repositories import ClienteRepository
from mongo.repositories import MascotaRepository

class ClienteService:
    def __init__(self, cliente_repo: ClienteRepository, mascota_repo: MascotaRepository):
        self.cliente_repo = cliente_repo
        self.mascota_repo = mascota_repo

    def get_cliente(self, cliente_id: str):
        """
        Obtiene un cliente asegurándose de que exista.
        """
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente con ID {cliente_id} no encontrado")
        return cliente


    def eliminar_cliente(self, cliente_id: str):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado")
        
        # Eliminar mascotas asociadas
        self.mascota_repo.delete_by_cliente_id(cliente_id)

        # Eliminar cliente
        self.cliente_repo.delete(cliente_id)

    def actualizar_cliente(self, cliente_id: str, cliente: dict):
        # Validar que el cliente existe antes de actualizar
        existente = self.cliente_repo.get_by_id(cliente_id)
        if not existente:
            raise ValueError("Cliente no encontrado")

        # Realizar la actualización
        return self.cliente_repo.update(cliente_id, cliente)
