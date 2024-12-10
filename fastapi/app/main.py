from fastapi import FastAPI
from app.routers.clientes import router as clientes_router
from app.routers.mascotas import router as mascotas_router
 

# Crear instancia de la aplicación FastAPI
app = FastAPI()

# Registrar los routers
app.include_router(clientes_router, prefix="/api")
app.include_router(mascotas_router, prefix="/clientes/{cliente_id}/mascotas", tags=["mascotas"])

# Ruta de inicio
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API SOLID"}

# Ruta principal de salud
@app.get("/", tags=["Health"])
async def health_check():
    return {"message": "API funcionando correctamente"}