from mongo.database import clientes_collection
from bson import ObjectId
import uuid

def create_cliente(cliente: dict):
    # Generar un ID si no se proporciona
    if "id" not in cliente or cliente["id"] is None:
        cliente["id"] = str(uuid.uuid4())  # Genera un UUID como string

    result = clientes_collection.insert_one(cliente)  # Inserta el cliente en MongoDB
    cliente["_id"] = str(result.inserted_id)  # Agrega el ObjectId para referencia interna
    return cliente

def get_cliente(cliente_id: str):
    cliente = clientes_collection.find_one({"id": cliente_id}, {"_id": 0})  # Buscar por `id` legible
    return cliente



def get_clientes(skip: int = 0, limit: int = 10):
    clientes = list(clientes_collection.find().skip(skip).limit(limit))
    for cliente in clientes:
        cliente["_id"] = str(cliente["_id"])
    return clientes


def add_mascota(cliente_id: str, mascota: dict):
    # Generar un ID legible para la mascota si no existe
    if "id" not in mascota or mascota["id"] is None:
        mascota["id"] = str(uuid.uuid4())  # Genera un UUID como string

    # Agregar la mascota al cliente
    result = clientes_collection.update_one(
        {"id": cliente_id},  # Buscar cliente por `id`
        {"$push": {"mascotas": mascota}}
    )
    if result.matched_count == 0:
        return None
    return mascota



def update_cliente(cliente_id: str, cliente_data: dict):
    result = clientes_collection.update_one(
        {"id": cliente_id},  # Buscar por `id` legible
        {"$set": cliente_data}  # Actualizar los datos
    )
    return result.modified_count > 0



def update_mascota(cliente_id: str, mascota_id: str, mascota_data: dict):
    cliente = clientes_collection.find_one({"id": cliente_id})
    if not cliente:
        return None

    # Actualizar los campos específicos de la mascota
    result = clientes_collection.update_one(
        {"id": cliente_id, "mascotas.id": mascota_id},  # Buscar por `id` del cliente y mascota
        {"$set": {f"mascotas.$.{k}": v for k, v in mascota_data.items()}}
    )
    return result.modified_count > 0


def delete_cliente(cliente_id: str):
    result = clientes_collection.delete_one({"id": cliente_id})  # Buscar por `id`
    return result.deleted_count > 0


def delete_mascota(cliente_id: str, mascota_id: str):
    result = clientes_collection.update_one(
        {"id": cliente_id},
        {"$pull": {"mascotas": {"id": mascota_id}}}  # Buscar por `id` de la mascota
    )
    return result.modified_count > 0
