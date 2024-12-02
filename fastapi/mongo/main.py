from fastapi import FastAPI
from app.routers import clientes

# Crear instancia de la aplicación FastAPI
app = FastAPI()

# Registrar los routers
app.include_router(clientes.router, prefix="/api", tags=["Clientes"])

# Ruta de inicio
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API SOLID"}
