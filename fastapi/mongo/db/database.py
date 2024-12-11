from mongo.db.connection import MongoConnectionManager

# Configura la URI y el nombre de la base de datos
MONGO_URI = "mongodb+srv://aristeolg:clinicaVetGr4@cluster0.uylyg.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "mi_base_de_datos"

# Inicializa la conexión
db = MongoConnectionManager.connect(MONGO_URI, DATABASE_NAME)

# Colecciones específicas
clientes_collection = MongoConnectionManager.get_collection("clientes")
mascotas_collection = MongoConnectionManager.get_collection("mascotas")
citas_collection = MongoConnectionManager.get_collection("citas")
facturas_collection = MongoConnectionManager.get_collection("facturas")
