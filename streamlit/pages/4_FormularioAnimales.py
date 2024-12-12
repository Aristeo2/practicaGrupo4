
import streamlit as st
import requests
import pandas as pd
import logging
from datetime import datetime
from DatosMascota import VerificarMascota  # Importar funciones de validación

API_URL = "http://fastapi:8000"  # URL de la API de FastAPI

# Configuración de logging
logging.basicConfig(
    filename='formulario_mascotas.log',  # Ruta del archivo de log
    level=logging.INFO,  # Registra eventos de nivel INFO o superior
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato del log
)

st.title("Formulario de Mascotas")

# Funciones auxiliares para consumir la API
def get_clientes():
    try:
        response = requests.get(f"{API_URL}/clientes/")
        response.raise_for_status()
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al obtener clientes: {e}")
        st.error("Error al obtener clientes.")
        return []

def create_cliente(cliente):
    try:
        response = requests.post(f"{API_URL}/clientes/", json=cliente)
        response.raise_for_status()
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al crear cliente: {e}")
        st.error("Error al registrar el cliente.")
        return None

def get_mascotas():
    try:
        response = requests.get(f"{API_URL}/mascotas/")
        response.raise_for_status()
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al obtener mascotas: {e}")
        st.error("Error al obtener las mascotas.")
        return []

def create_mascota(mascota):
    try:
        response = requests.post(f"{API_URL}/mascotas/", json=mascota)
        response.raise_for_status()
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al crear mascota: {e}")
        st.error("Error al crear la mascota.")
        return None

# Encabezado
st.header("Mascotas")

# Crear nueva mascota
st.subheader("Crear nueva mascota")

nombre_mascota = st.text_input("Nombre de la Mascota")
especie = st.selectbox("Especie", ["Perro", "Gato"])
raza = st.text_input("Raza")
fecha_nacimiento = st.date_input("Fecha de Nacimiento")
patologias = st.text_input("Patologías")
cliente_id = st.text_input("ID del Dueño")

if st.button("Guardar Mascota"):
    logging.info(f"Intentando guardar la mascota: {nombre_mascota}, ID del dueño: {cliente_id}")

    # Verificar que el ID del dueño existe en la lista de clientes
    clientes = get_clientes()
    dueño_existe = any(cliente["_id"] == str(cliente_id) for cliente in clientes)  # Verifica si el ID existe en la lista

    if not dueño_existe:
        st.error("El ID del dueño no existe. Por favor, introduzca un ID válido.")
        logging.error(f"ID del dueño {cliente_id} no encontrado.")
    elif VerificarMascota.nombre(nombre_mascota) and VerificarMascota.raza(raza) and VerificarMascota.patologias(patologias):
        fecha_nacimiento_datetime = datetime.combine(fecha_nacimiento, datetime.min.time())
        mascota = {
            "id_cliente": cliente_id,
            "nombre": nombre_mascota,
            "especie": especie,
            "raza": raza,
            "fecha_nacimiento": fecha_nacimiento_datetime.isoformat(),
            "patologias": patologias,
            
        }
        nueva_mascota = create_mascota(mascota)
        if nueva_mascota:
            st.success("Mascota creada con éxito")
            logging.info(f"Mascota '{nombre_mascota}' creada exitosamente con ID de dueño: {cliente_id}.")
        else:
            st.error("Error al crear la mascota")
            logging.error("Error al crear la mascota.")
    else:
        st.error("Datos mal introducidos")
        logging.error(f"Datos inválidos para la mascota: {nombre_mascota}, raza: {raza}, patologías: {patologias}")
         
# Mostrar lista de clientes registrados
st.subheader("Lista de Clientes Registrados")
clientes = get_clientes()
if clientes:
    df_clientes = pd.DataFrame(clientes)  # Convertir a DataFrame de Pandas
    st.table(df_clientes)  # Mostrar tabla
else:
    st.warning("No hay clientes registrados") 

# Mostrar lista de mascotas
st.subheader("Lista de Mascotas")
mascotas = get_mascotas()
if mascotas:
    for mascota in mascotas:
        st.write(mascota)
else:
    st.warning("No hay mascotas registradas")
