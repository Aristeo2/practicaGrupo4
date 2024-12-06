# app/services/cliente_service.py
from typing import List, Optional
from app.schemas.schemas import Cliente
from app.db.database import Database

class ClienteService:
    def __init__(self):
        self.db = Database().get_collection("clientes")

    def create_cliente(self, cliente: Cliente) -> Cliente:
        cliente_dict = cliente.dict()
        result = self.db.insert_one(cliente_dict)
        cliente_dict["_id"] = str(result.inserted_id)
        return Cliente(**cliente_dict)

    def get_all_clientes(self) -> List[Cliente]:
        clientes = self.db.find()
        return [Cliente(**cliente) for cliente in clientes]

    def get_cliente_by_id(self, cliente_id: str) -> Optional[Cliente]:
        cliente = self.db.find_one({"_id": cliente_id})
        if cliente:
            return Cliente(**cliente)
        return None

    def update_cliente(self, cliente_id: str, cliente: Cliente) -> Optional[Cliente]:
        cliente_dict = cliente.dict()
        result = self.db.update_one({"_id": cliente_id}, {"$set": cliente_dict})
        if result.modified_count > 0:
            updated_cliente = self.db.find_one({"_id": cliente_id})
            return Cliente(**updated_cliente)
        return None

    def delete_cliente(self, cliente_id: str) -> bool:
        result = self.db.delete_one({"_id": cliente_id})
        return result.deleted_count > 0
