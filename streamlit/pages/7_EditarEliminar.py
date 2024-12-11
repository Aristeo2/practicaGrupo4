import streamlit as st
import requests
import pandas as pd

# Base URL para FastAPI
API_BASE_URL = "http://fastapi:8000"

st.title("Editar o Eliminar Clientes y Mascotas")

# Funciones auxiliares para interactuar con la API
def get_clientes():
    response = requests.get(f"{API_BASE_URL}/clientes/")
    return response.json() if response.status_code == 200 else []

def get_mascotas(cliente_id):
    response = requests.get(f"{API_BASE_URL}/clientes/{cliente_id}/mascotas/")
    return response.json() if response.status_code == 200 else []

def update_cliente(cliente_id, cliente):
    response = requests.put(f"{API_BASE_URL}/clientes/{cliente_id}", json=cliente)
    return response.status_code == 200

def delete_cliente(cliente_id):
    response = requests.delete(f"{API_BASE_URL}/clientes/{cliente_id}")
    return response.status_code == 200

def update_mascota(cliente_id, mascota_id, mascota):
    response = requests.put(f"{API_BASE_URL}/clientes/{cliente_id}/mascotas/{mascota_id}", json=mascota)
    return response.status_code == 200

def delete_mascota(cliente_id, mascota_id):
    response = requests.delete(f"{API_BASE_URL}/clientes/{cliente_id}/mascotas/{mascota_id}")
    return response.status_code == 200

# Paso 1: Mostrar lista de clientes
st.subheader("Selecciona un cliente")
clientes = get_clientes()
if clientes:
    df_clientes = pd.DataFrame(clientes)
    cliente_seleccionado = st.selectbox("Selecciona un cliente", df_clientes["nombre"])
    cliente_id = df_clientes[df_clientes["nombre"] == cliente_seleccionado]["id"].values[0]

    # Paso 2: Mostrar mascotas del cliente seleccionado
    st.subheader(f"Mascotas de {cliente_seleccionado}")
    mascotas = get_mascotas(cliente_id)
    if mascotas:
        df_mascotas = pd.DataFrame(mascotas)
        mascota_seleccionada = st.selectbox("Selecciona una mascota", df_mascotas["nombre"])
        mascota_id = df_mascotas[df_mascotas["nombre"] == mascota_seleccionada]["id"].values[0]
    else:
        st.warning("Este cliente no tiene mascotas registradas.")
        mascota_seleccionada = None

    # Paso 3: Opciones de edición o eliminación
    operacion = st.radio("Selecciona una operación", ["Editar Cliente", "Eliminar Cliente", "Editar Mascota", "Eliminar Mascota"])

    if operacion == "Editar Cliente":
        st.subheader("Editar información del cliente")
        nuevo_nombre = st.text_input("Nuevo Nombre", value=cliente_seleccionado)
        nuevo_email = st.text_input("Nuevo Email", value=df_clientes[df_clientes["id"] == cliente_id]["email"].values[0])
        if st.button("Actualizar Cliente"):
            actualizado = update_cliente(cliente_id, {"nombre": nuevo_nombre, "email": nuevo_email})
            if actualizado:
                st.success("Cliente actualizado con éxito")
            else:
                st.error("Error al actualizar cliente")

    elif operacion == "Eliminar Cliente":
        st.subheader("Eliminar Cliente")
        if st.button(f"Eliminar {cliente_seleccionado}"):
            eliminado = delete_cliente(cliente_id)
            if eliminado:
                st.success("Cliente eliminado con éxito")
            else:
                st.error("Error al eliminar cliente")

    elif operacion == "Editar Mascota" and mascota_seleccionada:
        st.subheader("Editar información de la mascota")
        nueva_raza = st.text_input("Nueva Raza", value=df_mascotas[df_mascotas["id"] == mascota_id]["raza"].values[0])
        if st.button("Actualizar Mascota"):
            actualizado = update_mascota(cliente_id, mascota_id, {"raza": nueva_raza})
            if actualizado:
                st.success("Mascota actualizada con éxito")
            else:
                st.error("Error al actualizar mascota")

    elif operacion == "Eliminar Mascota" and mascota_seleccionada:
        st.subheader("Eliminar Mascota")
        if st.button(f"Eliminar {mascota_seleccionada}"):
            eliminado = delete_mascota(cliente_id, mascota_id)
            if eliminado:
                st.success("Mascota eliminada con éxito")
            else:
                st.error("Error al eliminar mascota")
else:
    st.warning("No hay clientes registrados.")
