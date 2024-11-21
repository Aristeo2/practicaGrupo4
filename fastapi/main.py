from fastapi import FastAPI, HTTPException
from crud import create_cliente, get_cliente, add_mascota, update_cliente, update_mascota, delete_cliente, delete_mascota
from schemas import Cliente, Mascota

app = FastAPI()


@app.post("/clientes/", response_model=Cliente)
def create_cliente_endpoint(cliente: Cliente):
    nuevo_cliente = create_cliente(cliente.dict())
    return nuevo_cliente

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def get_cliente_endpoint(cliente_id: str):
    cliente = get_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.post("/clientes/{cliente_id}/mascotas/", response_model=Mascota)
def add_mascota_endpoint(cliente_id: str, mascota: Mascota):
    nueva_mascota = add_mascota(cliente_id, mascota.dict())
    if not nueva_mascota:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return nueva_mascota

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def update_cliente_endpoint(cliente_id: str, cliente: Cliente):
    cliente_actualizado = update_cliente(cliente_id, cliente.dict())
    if not cliente_actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente_actualizado

@app.put("/clientes/{cliente_id}/mascotas/{mascota_id}")
def update_mascota_endpoint(cliente_id: str, mascota_id: str, mascota: Mascota):
    actualizado = update_mascota(cliente_id, mascota_id, mascota.dict())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Cliente o mascota no encontrados")
    return {"detail": "Mascota actualizada"}

@app.delete("/clientes/{cliente_id}")
def delete_cliente_endpoint(cliente_id: str):
    eliminado = delete_cliente(cliente_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"detail": "Cliente eliminado exitosamente"}

@app.delete("/clientes/{cliente_id}/mascotas/{mascota_id}")
def delete_mascota_endpoint(cliente_id: str, mascota_id: str):
    eliminado = delete_mascota(cliente_id, mascota_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente o mascota no encontrados")
    return {"detail": "Mascota eliminada exitosamente"}
