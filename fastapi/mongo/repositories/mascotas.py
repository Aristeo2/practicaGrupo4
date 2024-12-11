from mongo.repositories.base import BaseRepository

class MascotaRepository(BaseRepository):
    def delete_by_cliente_id(self, cliente_id: str):
        """Elimina todas las mascotas asociadas a un cliente."""
        return self.collection.delete_many({"id_cliente": cliente_id})
