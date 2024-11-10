
import streamlit as st
import requests
from datetime import datetime
from  DatosMascota import VerificarMascota  # Importar funciones de validación


API_URL = "http://127.0.0.1:8000"  # URL de la API de FastAPI

st.title("Gestión de Clientes y Mascotas")

# Selección de funcionalidad
seccion = st.sidebar.selectbox("Seleccione una sección", ("Clientes", "Mascotas"))

# Funciones auxiliares para consumir la API
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


st.header("Mascotas")

    # Crear nueva mascota
st.subheader("Crear nueva mascota")

nombre_mascota = st.text_input("Nombre de la Mascota")
especie = st.selectbox("Especie", ["Perro", "Gato"])
raza = st.text_input("Raza")
fecha_nacimiento = st.date_input("Fecha de Nacimiento")
patologias = st.text_input("Patologías")
dueño_id = st.number_input("ID del Dueño", min_value=1, step=1)

if st.button("Guardar Mascota"):
    if VerificarMascota.nombre(nombre_mascota) and VerificarMascota.raza(raza) and VerificarMascota.patologias(patologias):
        mascota = {
            "nombre": nombre_mascota,
            "especie": especie,
            "raza": raza,
            "fecha_nacimiento": str(fecha_nacimiento),
            "patologias": patologias,
            "dueño": dueño_id
            }
        nueva_mascota = create_mascota(mascota)
        if nueva_mascota:
            st.success("Mascota creada con éxito")
        else:
            st.error("Error al crear la mascota")

    # Mostrar lista de mascotas
st.subheader("Lista de Mascotas")
mascotas = get_mascotas()
if mascotas:
    for mascota in mascotas:
        st.write(mascota)
else:
    st.warning("No hay mascotas registradas")

