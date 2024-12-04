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

# Ruta principal de salud
@app.get("/", tags=["Health"])
async def health_check():
    return {"message": "API funcionando correctamente"}