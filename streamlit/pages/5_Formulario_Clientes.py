# Importación de clase para verificar datos de cliente

import streamlit as st
from datos_cliente.datoscliente import Verificar_Cliente
import requests


API_URL = "http://fastapi:8000"  # URL de la API de FastAPI




# Funciones auxiliares para consumir la API


def get_clientes():
    try:
        response = requests.get(f"{API_URL}/clientes/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener clientes: {e}")
        return []
    
def create_cliente(cliente):
    try:
        response = requests.post(f"{API_URL}/clientes/", json=cliente)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al registrar cliente: {e}")
        return None


# Título
st.title("Formulario de Registro de Personas")


st.header("Información del Dueño")

# Nombre
nombre = st.text_input("Nombre del Dueño")

# DNI   
dni = st.text_input("DNI del Dueño")

# Direccion
direccion = st.text_area("Dirección del Dueño")

# Relefono
telefono = st.text_input("Teléfono del Dueño")

# @Correo
email = st.text_input("Correo Electrónico del Dueño")

# Botón 
if st.button("Registrar Dueño"):
    resultados = Verificar_Cliente.verificar_formulario(nombre, dni, direccion, telefono, email)
    
    # Comprobamos si todos los campos son válidos
    errores = [mensaje for campo, (valido, mensaje) in resultados.items() if not valido]

    if errores:
        # Mostramos los mensajes de error para cada campo no válido
        for error in errores:
            st.error(error)
    else:
        # Si todos los campos son válidos, mostramos la información registrada
        cliente = {
            "nombre" : nombre,
            "dni" : dni,
            "direccion": direccion,
            "tlf": telefono,
            "email" : email,
        }
        
        nuevo_cliente = create_cliente(cliente)
        if nuevo_cliente:
            st.success("¡Dueño registrado exitosamente!")
            st.write("Información del Dueño:")
            st.write(f"**Nombre:** {nombre}")
            st.write(f"**DNI:** {dni}")
            st.write(f"**Dirección:** {direccion}")
            st.write(f"**Teléfono:** {telefono}")
            st.write(f"**Correo Electrónico:** {email}")
        else:
            st.error("Error al crear el cliente")
      

st.subheader("Lista de Clientes")
clientes = get_clientes()
if clientes:
    for cliente in clientes:
        st.write(cliente)
else:
    st.warning("No hay mascotas registradas")