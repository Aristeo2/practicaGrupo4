from mongo.database import clientes_collection, citas_collection
from app.schemas import Cita
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

#Citas

def create_cita(cita: Cita):
    cita_dict = cita.dict()
    cita_dict["_id"] = str(ObjectId())
    citas_collection.insert_one(cita_dict)
    return cita_dict


# Obtener todas las citas
def get_citas():
    citas = list(citas_collection.find())
    for cita in citas:
        cita["_id"] = str(cita["_id"])
    return citas


# Obtener una cita por ID
def get_cita(cita_id: str):
    cita = citas_collection.find_one({"_id": ObjectId(cita_id)})
    if cita:
        cita["_id"] = str(cita["_id"])
    return cita


# Actualizar una cita por ID
def update_cita(cita_id: str, cita_data: dict):
    result = citas_collection.update_one({"_id": ObjectId(cita_id)}, {"$set": cita_data})
    return result.modified_count > 0


# Eliminar una cita por ID
def delete_cita(cita_id: str):
    result = citas_collection.delete_one({"_id": ObjectId(cita_id)})
    return result.deleted_count > 0
