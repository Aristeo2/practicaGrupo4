from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson.json_util import dumps
import pandas as pd
import numpy as np
from mongo.db.database import contratos_collection
from mongo.repositories.contrato import ContratosRepository
import json

# Configurar el router
router = APIRouter()
contrato_repo = ContratosRepository(contratos_collection)

@router.get("/")
def get_all_contratos():
    """
    Obtener todos los contratos.
    """
    contratos = contrato_repo.list_all()

    # Limpiar datos no válidos
    for contrato in contratos:
        for key, value in contrato.items():
            if isinstance(value, float) and (pd.isna(value) or np.isinf(value)):
                contrato[key] = None  # Reemplazar NaN, Inf o -Inf con None
    
    return contratos
