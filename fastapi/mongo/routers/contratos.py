from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson.json_util import dumps
from mongo.db.database import contratos_collection
from mongo.repositories.contrato import ContratosRepository
import json

# Configurar el router
router = APIRouter()
contrato_repo = ContratosRepository(contratos_collection)

@router.get("/")
def get_all_contratos():
    """
    Obtener todas las mascotas.
    """
    contratos = contrato_repo.list_all()
    return contratos