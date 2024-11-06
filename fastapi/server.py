import shutil

import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile,Form, HTTPException
import pandas as pd
import csv
from typing import  List

from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Contrato(BaseModel):
    #titulo:str
    #autor:str
    #pais:str
    #genero:str
    fecha:str
    centro_seccion:str
    nreg:str
    nexp:str
    objeto:str
    tipo:str
    procedimiento:str
    numlicit:str
    numinvitcurs:str
    proc_adjud:str
    presupuesto_con_iva:str
    valor_estimado:str
    importe_adj_con_iva:str
    adjuducatario:str
    fecha_formalizacion:str
    I_G:str


class ListadoContratos(BaseModel):
    contratos = List[Contrato]

app = FastAPI(
    title="Servidor de datos",
    description="""Servimos datos de contratos, pero podríamos hacer muchas otras cosas, la la la.""",
    version="0.1.0",
)


@app.get("/retrieve_data/")
def retrieve_data ():
    todosmisdatos = pd.read_csv('./contratos_inscritos_simplificado_2023.csv',sep=';')
    todosmisdatos = todosmisdatos.fillna(0)
    todosmisdatosdict = todosmisdatos.to_dict(orient='records')
    listado = ListadoContratos()
    listado.contratos = todosmisdatosdict
    return listado

class FormData(BaseModel):
    date: str
    description: str
    option: str
    amount: float

@app.post("/envio/")
async def submit_form(data: FormData):
    return {"message": "Formulario recibido", "data": data}

### GESTIÓN DE CLIENTES Y MASCOTAS

# Definimos las rutas de los archivos csv

CLIENTES_CSV = "clientes.csv"
MASCOTAS_CSV = "mascotas.csv"

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