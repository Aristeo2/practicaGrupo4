from mongo.database import clientes_collection
from bson import ObjectId


def create_cliente(cliente: dict):
    result = clientes_collection.insert_one(cliente)
    cliente["_id"] = result.inserted_id  # Asigna el `_id` generado por MongoDB
    return cliente

def get_cliente(cliente_id: str):
    cliente = clientes_collection.find_one({"_id": ObjectId(cliente_id)})
    if cliente:
        cliente["_id"] = str(cliente["_id"])  # Convertir `_id` a cadena
    return cliente


def get_clientes(skip: int = 0, limit: int = 10):
    clientes = list(clientes_collection.find().skip(skip).limit(limit))
    for cliente in clientes:
        cliente["_id"] = str(cliente["_id"])
    return clientes


def add_mascota(cliente_id: str, mascota: dict):
    mascota["_id"] = ObjectId()  # Genera un nuevo `_id` para la mascota
    result = clientes_collection.update_one(
        {"_id": ObjectId(cliente_id)},
        {"$push": {"mascotas": mascota}}
    )
    if result.matched_count == 0:
        return None
    return mascota


def update_cliente(cliente_id: str, cliente_data: dict):
    cliente_data = {k: v for k, v in cliente_data.items() if v is not None}
    result = clientes_collection.update_one(
        {"_id": ObjectId(cliente_id)},
        {"$set": cliente_data}
    )
    if result.matched_count == 0:
        return None
    return get_cliente(cliente_id)


def update_mascota(cliente_id: str, mascota_id: str, mascota_data: dict):
    cliente = clientes_collection.find_one({"_id": ObjectId(cliente_id)})
    if not cliente:
        return None
    result = clientes_collection.update_one(
        {"_id": ObjectId(cliente_id), "mascotas._id": ObjectId(mascota_id)},
        {"$set": {f"mascotas.$.{k}": v for k, v in mascota_data.items()}}
    )
    return result.modified_count > 0

def delete_cliente(cliente_id: str):
    result = clientes_collection.delete_one({"_id": ObjectId(cliente_id)})
    return result.deleted_count > 0

def delete_mascota(cliente_id: str, mascota_id: str):
    result = clientes_collection.update_one(
        {"_id": ObjectId(cliente_id)},
        {"$pull": {"mascotas": {"_id": ObjectId(mascota_id)}}}
    )
    return result.modified_count > 0
