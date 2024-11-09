
import streamlit as st
import requests
from datetime import datetime
from  DatosMascota import VerificarMascota  # Importar funciones de validación

API_URL = "http://127.0.0.1:8000"  # Dirección de la API FastAPI

# Funciones para interactuar con la API
def obtener_clientes(nombre_dueño=""):
    response = requests.get(f"{API_URL}/clientes/")
    if response.status_code == 200:
        clientes = response.json()
        if nombre_dueño:
            return [c for c in clientes if nombre_dueño.lower() in c["nombre"].lower()]
        return clientes
    else:
        return []

def agregar_mascota(nombre, especie, raza, fecha_nacimiento, patologias, dueño_id):
    mascota = {
        "id": len(obtener_mascotas()) + 1,
        "nombre": nombre,
        "especie": especie,
        "raza": raza,
        "fecha_nacimiento": fecha_nacimiento,
        "patologias": patologias,
        "dueño_id": dueño_id
    }
    response = requests.post(f"{API_URL}/mascotas/", json=mascota)
    return response.json() if response.status_code == 200 else None

def obtener_mascotas():
    response = requests.get(f"{API_URL}/mascotas/")
    return response.json() if response.status_code == 200 else []

# Interfaz de usuario para el formulario de mascotas
st.title("Formulario de Registro de Mascota")

with st.form("formulario_mascota"):
    nombre = st.text_input("Nombre de la Mascota")
    especie = st.selectbox("Especie", ["perro", "gato"])
    raza = st.text_input("Raza")
    fecha_nacimiento = st.date_input("Fecha de Nacimiento")
    patologias = st.text_area("Patologías Previas")

    # Buscar dueño
    st.subheader("Buscar Dueño")
    nombre_dueño = st.text_input("Buscar Dueño (por nombre)")
    
    # Validar entrada de datos usando las funciones de VerificarMascota
    if not VerificarMascota.nombre(nombre):
        st.warning("El nombre de la mascota debe iniciar con mayúscula y solo incluir letras y espacios.")
        
    if not VerificarMascota.tipo(especie.capitalize()):
        st.warning("La especie debe ser 'Perro' o 'Gato'.")
        
    if not VerificarMascota.raza(raza):
        st.warning("La raza debe tener menos de 20 caracteres, solo letras y comenzar con mayúscula.")
        
    fecha_nacimiento_str = fecha_nacimiento.strftime("%d/%m/%Y")
    if not VerificarMascota.fecha_nacimiento(fecha_nacimiento_str):
        st.warning("La fecha de nacimiento debe estar en formato DD/MM/YYYY.")
        
    if patologias and not VerificarMascota.patologias(patologias):
        st.warning("Las patologías deben comenzar con mayúscula y no contener caracteres especiales ni números.")
    
    # Buscar dueños en la API y mostrar resultados
    dueños = []
    dueño_id = None
    if nombre_dueño:
        dueños = obtener_clientes(nombre_dueño)
        if dueños:
            dueño_seleccionado = st.selectbox("Seleccione un dueño", [f"{d['id']} - {d['nombre']}" for d in dueños])
            dueño_id = int(dueño_seleccionado.split(" - ")[0])
        else:
            st.warning("No se encontraron dueños con ese nombre.")
    
    # Enviar formulario
    if st.form_submit_button("Guardar Mascota"):
        if not VerificarMascota.nombre(nombre) or not dueño_id:
            st.error("Por favor, complete todos los campos obligatorios con el formato correcto.")
        else:
            nueva_mascota = agregar_mascota(nombre, especie, raza, fecha_nacimiento_str, patologias, dueño_id)
            if nueva_mascota:
                st.success("Mascota registrada exitosamente.")
            else:
                st.error("Error al registrar la mascota.")
