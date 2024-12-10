from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import csv
from modelo import Cliente, Mascota

app = FastAPI()

# Definimos las rutas de los archivos csv
CLIENTES_CSV = "clientes.csv"
MASCOTAS_CSV = "mascotas.csv"
CONTRATOS_CSV = "contratos_inscritos_simplificado2023.csv"  # Nueva constante para el archivo de contratos

# Funciones de ayuda para leer y escribir en los CSV
def read_csv(file_path):
    return pd.read_csv(file_path)

def write_csv(data, file_path):
    data.to_csv(file_path, index=False, quoting=csv.QUOTE_NONNUMERIC)

# Operaciones CRUD para Clientes
@app.get("/clientes/")
async def get_clientes():
    data = read_csv(CLIENTES_CSV)
    return data.to_dict(orient="records")

@app.get("/clientes/{cliente_id}")
async def get_cliente(cliente_id: int):
    data = read_csv(CLIENTES_CSV)
    cliente = data[data['id'] == cliente_id]
    if cliente.empty:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return cliente.to_dict(orient="records")[0]

@app.post("/clientes/")
async def create_cliente(cliente: Cliente):
    data = read_csv(CLIENTES_CSV)
    if cliente.id in data['id'].values:
        raise HTTPException(status_code=400, detail="ID already exists")
    new_cliente = pd.DataFrame([cliente.dict()])
    data = pd.concat([data, new_cliente], ignore_index=True)
    write_csv(data, CLIENTES_CSV)
    return cliente

@app.put("/clientes/{cliente_id}")
async def update_cliente(cliente_id: int, cliente: Cliente):
    data = read_csv(CLIENTES_CSV)
    if cliente_id not in data['id'].values:
        raise HTTPException(status_code=404, detail="Cliente not found")
    data.loc[data['id'] == cliente_id, ['nombre', 'dni', 'direccion', 'tlf', 'email']] = \
        [cliente.nombre, cliente.dni, cliente.direccion, cliente.tlf, cliente.email]
    write_csv(data, CLIENTES_CSV)
    return cliente

@app.delete("/clientes/{cliente_id}")
async def delete_cliente(cliente_id: int):
    data = read_csv(CLIENTES_CSV)
    data = data[data['id'] != cliente_id]
    write_csv(data, CLIENTES_CSV)
    return {"detail": "Cliente deleted"}

# Operaciones CRUD para Mascotas
@app.get("/mascotas/")
async def get_mascotas():
    data = read_csv(MASCOTAS_CSV)
    return data.to_dict(orient="records")

@app.get("/mascotas/{mascota_id}")
async def get_mascota(mascota_id: int):
    data = read_csv(MASCOTAS_CSV)
    mascota = data[data['id'] == mascota_id]
    if mascota.empty:
        raise HTTPException(status_code=404, detail="Mascota not found")
    return mascota.to_dict(orient="records")[0]

@app.post("/mascotas/")
async def create_mascota(mascota: Mascota):
    data = read_csv(MASCOTAS_CSV)
    if mascota.id in data['id'].values:
        raise HTTPException(status_code=400, detail="ID already exists")
    new_mascota = pd.DataFrame([mascota.dict()])
    data = pd.concat([data, new_mascota], ignore_index=True)
    write_csv(data, MASCOTAS_CSV)
    return mascota

@app.put("/mascotas/{mascota_id}")
async def update_mascota(mascota_id: int, mascota: Mascota):
    data = read_csv(MASCOTAS_CSV)
    if mascota_id not in data['id'].values:
        raise HTTPException(status_code=404, detail="Mascota not found")
    data.loc[data['id'] == mascota_id, ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'patologias', 'dueño']] = \
        [mascota.nombre, mascota.especie, mascota.raza, mascota.fecha_nacimiento, mascota.patologias, mascota.dueño]
    write_csv(data, MASCOTAS_CSV)
    return mascota

@app.delete("/mascotas/{mascota_id}")
async def delete_mascota(mascota_id: int):
    data = read_csv(MASCOTAS_CSV)
    data = data[data['id'] != mascota_id]
    write_csv(data, MASCOTAS_CSV)
    return {"detail": "Mascota deleted"}

# Operaciones CRUD para Contratos
@app.get("/contratos/")
async def get_contratos():
    data = read_csv(CONTRATOS_CSV)
    return data.to_dict(orient="records")

@app.get("/contratos/{contrato_id}")
async def get_contrato(contrato_id: int):
    data = read_csv(CONTRATOS_CSV)
    contrato = data[data['id'] == contrato_id]
    if contrato.empty:
        raise HTTPException(status_code=404, detail="Contrato not found")
    return contrato.to_dict(orient="records")[0]
