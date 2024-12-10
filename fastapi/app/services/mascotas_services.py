# app/services/mascotas_services.py
from bson import ObjectId
from app.db.database import Database
from fastapi import HTTPException

class MascotasService:
    def __init__(self):
        self.db = Database().get_collection("clientes")  # Trabajamos sobre la colección de clientes

    def add_mascota_to_cliente(self, cliente_id, mascota_data):
        mascota_data["_id"] = str(ObjectId())  # Generar un ID único para la mascota
        result = self.db.update_one(
            {"_id": ObjectId(cliente_id)},
            {"$push": {"mascotas": mascota_data}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return mascota_data

    def get_mascotas_by_cliente(self, cliente_id):
        cliente = self.db.find_one({"_id": ObjectId(cliente_id)})
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente.get("mascotas", [])

    def get_mascota_by_id(self, cliente_id, mascota_id):
        cliente = self.db.find_one({"_id": ObjectId(cliente_id)})
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        mascota = next(
            (m for m in cliente.get("mascotas", []) if m["_id"] == mascota_id), None
        )
        if not mascota:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        return mascota

    def update_mascota(self, cliente_id, mascota_id, updated_data):
        result = self.db.update_one(
            {"_id": ObjectId(cliente_id), "mascotas._id": mascota_id},
            {"$set": {f"mascotas.$.{key}": value for key, value in updated_data.items()}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Mascota o cliente no encontrado")
        return {"message": "Mascota actualizada correctamente"}

    def delete_mascota(self, cliente_id, mascota_id):
        result = self.db.update_one(
            {"_id": ObjectId(cliente_id)},
            {"$pull": {"mascotas": {"_id": mascota_id}}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Mascota o cliente no encontrado")
        return {"message": "Mascota eliminada correctamente"}
