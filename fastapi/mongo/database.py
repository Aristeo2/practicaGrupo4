from pymongo import MongoClient


# Configuración de MongoDB
client = MongoClient("mongodb+srv://aristeolg:clinicaVetGr4@cluster0.uylyg.mongodb.net/?retryWrites=true&w=majority")
db = client["mi_base_de_datos"]

#Colecciones
clientes_collection = db["clientes"]
citas_collection = db["citas"]