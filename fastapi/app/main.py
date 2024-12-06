from fastapi import FastAPI
from app.routers.clientes import router as clientes_router 

# Crear instancia de la aplicación FastAPI
app = FastAPI()

# Registrar los routers
app.include_router(clientes_router, prefix="/api")

# Ruta de inicio
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API SOLID"}

# Ruta principal de salud
@app.get("/", tags=["Health"])
async def health_check():
    return {"message": "API funcionando correctamente"}