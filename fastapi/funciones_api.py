import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile,Form, HTTPException
import pandas as pd
import csv
from typing import  List

def get_clientes():
    response = requests.get(f"{API_URL}/clientes/")
    return response.json() if response.status_code == 200 else []

def create_cliente(cliente):
    response = requests.post(f"{API_URL}/clientes/", json=cliente)
    return response.json() if response.status_code == 200 else None

def get_mascotas():
    response = requests.get(f"{API_URL}/mascotas/")
    return response.json() if response.status_code == 200 else []

def create_mascota(mascota):
    response = requests.post(f"{API_URL}/mascotas/", json=mascota)
    return response.json() if response.status_code == 200 else None