from pymongo import MongoClient


# Configuración de MongoDB
MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client["mi_base_de_datos"]
clientes_collection = db["clientes"]
