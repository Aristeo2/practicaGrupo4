#Formulario_Animales de Richi

import streamlit as st
import sqlite3
from datetime import datetime

# Configuración de conexión a la base de datos
conn = sqlite3.connect('clinica_veterinaria.db')
cursor = conn.cursor()

# Crear tabla de mascotas si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mascotas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        especie TEXT NOT NULL CHECK(especie IN ('perro', 'gato')),
        raza TEXT,
        fecha_nacimiento DATE,
        patologias TEXT,
        dueño_id INTEGER,
        FOREIGN KEY (dueño_id) REFERENCES dueños(id)
    )
''')

# Crear tabla de dueños si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dueños (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        direccion TEXT
    )
''')

conn.commit()

# Función para buscar dueños
def buscar_dueños(nombre_dueño):
    cursor.execute("SELECT id, nombre FROM dueños WHERE nombre LIKE ?", ('%' + nombre_dueño + '%',))
    return cursor.fetchall()

# Función para agregar mascota
def agregar_mascota(nombre, especie, raza, fecha_nacimiento, patologias, dueño_id):
    cursor.execute('''
        INSERT INTO mascotas (nombre, especie, raza, fecha_nacimiento, patologias, dueño_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, especie, raza, fecha_nacimiento, patologias, dueño_id))
    conn.commit()
    return cursor.lastrowid

# Función para actualizar opciones adicionales de la mascota
def actualizar_opciones(id_mascota, observaciones):
    cursor.execute('''
        UPDATE mascotas 
        SET patologias = COALESCE(patologias, '') || ', ' || ?
        WHERE id = ?
    ''', (observaciones, id_mascota))
    conn.commit()

# Recuperar parámetro de URL para identificar la página
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["form"])[0]
id_mascota = query_params.get("id_mascota", [None])[0]

# Página del formulario de mascota
if page == "form":
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
        
        # Buscar dueños en la base de datos y mostrar resultados
        dueños = []
        dueño_id = None
        if nombre_dueño:
            dueños = buscar_dueños(nombre_dueño)
            if dueños:
                dueño_seleccionado = st.selectbox("Seleccione un dueño", [f"{id} - {nombre}" for id, nombre in dueños])
                dueño_id = int(dueño_seleccionado.split(" - ")[0])
            else:
                st.warning("No se encontraron dueños con ese nombre.")
        
        # Enviar formulario
        if st.form_submit_button("Siguiente"):
            if not nombre or not dueño_id:
                st.error("Por favor, complete todos los campos obligatorios.")
            else:
                fecha_nacimiento_str = fecha_nacimiento.strftime("%Y-%m-%d")
                nuevo_id_mascota = agregar_mascota(nombre, especie, raza, fecha_nacimiento_str, patologias, dueño_id)
                
                # Redirigir a la página de opciones adicionales con id_mascota
                st.experimental_set_query_params(page="options", id_mascota=nuevo_id_mascota)
                st.experimental_rerun()

# Página de opciones adicionales
elif page == "options" and id_mascota is not None:
    id_mascota = int(id_mascota)
    st.title("Opciones Adicionales para la Mascota")
    
    # Recuperar y mostrar información de la mascota
    cursor.execute("SELECT nombre, especie FROM mascotas WHERE id = ?", (id_mascota,))
    mascota = cursor.fetchone()
    if mascota:
        st.write(f"Mascota: {mascota[0]} ({mascota[1]})")
    else:
        st.error("La mascota no se encontró en la base de datos.")
    
    # Opciones adicionales
    vacunas = st.checkbox("Vacunas completas")
    desparasitado = st.checkbox("Desparasitado")
    observaciones = st.text_area("Observaciones adicionales")
    
    # Guardar opciones adicionales
    if st.button("Guardar Opciones"):
        observaciones_final = "Vacunas completas, " if vacunas else ""
        observaciones_final += "Desparasitado, " if desparasitado else ""
        observaciones_final += observaciones
        
        actualizar_opciones(id_mascota, observaciones_final)
        st.success("Opciones adicionales guardadas exitosamente.")
        st.write("Volver al [inicio](?page=form)")

else:
    st.error("Página no encontrada. Vuelva al formulario principal.")



