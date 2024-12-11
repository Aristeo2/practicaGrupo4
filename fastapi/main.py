from fastapi import FastAPI
from mongo.routers.cliente import router as cliente_router
from mongo.routers.mascota import router as mascota_router
from mongo.routers.cita import router as cita_router
from mongo.routers.factura import router as factura_router
from mongo.middleware.middleware import ObjectIdMiddleware
from mongo.db.connection import MongoConnectionManager


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    MongoConnectionManager.connect(
        "mongodb+srv://aristeolg:clinicaVetGr4@cluster0.uylyg.mongodb.net/?retryWrites=true&w=majority",
        "mi_base_de_datos"
    )

@app.on_event("shutdown")
async def shutdown_event():
    MongoConnectionManager.close()

app.add_middleware(ObjectIdMiddleware)

# Registrar routers
app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])
app.include_router(mascota_router, prefix="/mascotas", tags=["Mascotas"])
app.include_router(factura_router, prefix="/facturas", tags=["Facturas"])
app.include_router(cita_router, prefix="/citas", tags=["Citas"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de la clínica veterinaria"}
