import streamlit as st
import requests
import pandas as pd

# Configuración de la URL de la API
API_URL = "http://fastapi:8000"  # Cambia esta URL si es necesario

# Funciones auxiliares para consumir la API
def get_clientes():
    """Obtiene la lista de clientes desde la API."""
    response = requests.get(f"{API_URL}/clientes/")
    return response.json() if response.status_code == 200 else []

def get_mascotas():
    """Obtiene la lista de mascotas desde la API."""
    response = requests.get(f"{API_URL}/mascotas/")
    return response.json() if response.status_code == 200 else []

# Título de la aplicación
st.title("Visualización de Clientes y Mascotas con Filtros de Búsqueda")

# Sección para visualizar clientes
st.header("Clientes Registrados")
clientes = get_clientes()

if clientes:
    # Convertir la lista de clientes en un DataFrame de Pandas
    df_clientes = pd.DataFrame(clientes)
    
    # Opciones de filtro
    st.subheader("Buscar Clientes")
    filtro_cliente_id = st.text_input("Buscar por ID de Cliente")
    filtro_cliente_nombre = st.text_input("Buscar por Nombre de Cliente")
    
    # Filtrar por ID de cliente
    if filtro_cliente_id:
        df_clientes = df_clientes[df_clientes["_id"].astype(str).str.contains(filtro_cliente_id, case=False)]
    
    # Filtrar por nombre de cliente
    if filtro_cliente_nombre:
        df_clientes = df_clientes[df_clientes["nombre"].str.contains(filtro_cliente_nombre, case=False)]
    
    # Mostrar los resultados filtrados
    if not df_clientes.empty:
        st.subheader("Resultados de Clientes")
        st.table(df_clientes)
    else:
        st.warning("No se encontraron clientes con los filtros aplicados.")
else:
    st.warning("No hay clientes registrados")

# Separador
st.markdown("---")

# Sección para visualizar mascotas
st.header("Mascotas Registradas")
mascotas = get_mascotas()

if mascotas:
    # Convertir la lista de mascotas en un DataFrame de Pandas
    df_mascotas = pd.DataFrame(mascotas)
    
    # Opciones de filtro
    st.subheader("Buscar Mascotas")
    filtro_mascota_id = st.text_input("Buscar por ID de Mascota")
    filtro_mascota_nombre = st.text_input("Buscar por Nombre de Mascota")
    filtro_dueño_id = st.text_input("Buscar por ID del Dueño")
    
    # Filtrar por ID de mascota
    if filtro_mascota_id:
        df_mascotas = df_mascotas[df_mascotas["_id"].astype(str).str.contains(filtro_mascota_id, case=False)]
    
    # Filtrar por nombre de mascota
    if filtro_mascota_nombre:
        df_mascotas = df_mascotas[df_mascotas["nombre"].str.contains(filtro_mascota_nombre, case=False)]
    
    # Filtrar por ID del dueño
    if filtro_dueño_id:
        df_mascotas = df_mascotas[df_mascotas["id_cliente"].astype(str).str.contains(filtro_dueño_id, case=False)]
    
    # Mostrar los resultados filtrados
    if not df_mascotas.empty:
        st.subheader("Resultados de Mascotas")
        st.table(df_mascotas)
    else:
        st.warning("No se encontraron mascotas con los filtros aplicados.")
else:
    st.warning("No hay mascotas registradas")