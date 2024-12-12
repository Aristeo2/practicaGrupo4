import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import requests
import uuid
import json
import os
import pandas as pd

API_URL = "http://fastapi:8000"

JSON_FILE = "citas.json"
FACTURAS_FILE = "facturas.json"

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
    response = requests.post(f"{API_URL}/clientes/", json=mascota)
    return response.json() if response.status_code == 200 else None

# Diccionario de tratamientos y subtratamientos
treatments = {
    "Análisis de sangre y hormonales": ["Vacunación", "Desparasitación"],
    "Revisión general": [],
    "Revisión específica": ["Cardiología", "Cutánea", "Broncológica"],
    "Ecografías": [],
    "Limpieza bucal": [],
    "Extracción de piezas dentales": [],
    "Cirugía": ["Castración", "Abdominal", "Cardíaca", "Articular y ósea", "Hernias"]
}


API_URL = "http://fastapi:8000"

def get_citas():
    """Obtiene todas las citas desde la API."""
    response = requests.get(f"{API_URL}/citas/")
    if response.status_code == 200:
        return response.json()
    st.error("Error al obtener las citas.")
    return []

def save_cita(cita):
    """Guarda una cita nueva mediante la API."""
    response = requests.post(f"{API_URL}/citas/", json=cita)
    if response.status_code == 200:
        return response.json()
    st.error("Error al guardar la cita.")
    return None

def delete_cita(cita_id):
    """Elimina una cita mediante la API."""
    response = requests.delete(f"{API_URL}/citas/{cita_id}")
    if response.status_code == 200:
        return response.json()
    st.error("Error al eliminar la cita.")
    return None


# Cargar citas al inicio desde la API
if "events" not in st.session_state:
    citas = get_citas()
    if not citas:
        st.error("No se pudieron cargar las citas desde la API.")
        st.session_state["events"] = []
    else:
        st.session_state["events"] = [
            {
                "id": str(cita["_id"]),  # Mapear _id a id
                "title": f"{cita.get('tratamiento', 'Tratamiento no especificado')} - {cita.get('cliente_id', 'ID desconocido')}",
                "start": cita.get("fecha_inicio", "Fecha no disponible"),
                "end": cita.get("fecha_fin", "Fecha no disponible"),
                "color": "#FF6347",
            }
            for cita in citas
        ]


if "main_treatment" not in st.session_state:
    st.session_state["main_treatment"] = list(treatments.keys())[0]

if "selected_sub_treatments" not in st.session_state:
    st.session_state["selected_sub_treatments"] = []

# Función para registrar una cita y agregarla al calendario
def register_appointment(cliente_id, mascota_id, fecha_inicio, fecha_fin, tratamiento, subtratamientos):
    """Registrar la cita y añadirla al calendario."""
    nueva_cita = {
        "cliente_id": cliente_id,
        "mascota_id": mascota_id,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "tratamiento": tratamiento,
        "sub_treatments": subtratamientos,
    }

    if check_appointment_conflict(fecha_inicio, fecha_fin, st.session_state["events"]):
        st.error("Error: El horario de la cita entra en conflicto con otra existente.")
        return False

    # Asignar un color según el tratamiento
    treatment_colors = {
        "Análisis de sangre y hormonales": "#FF6C6C",
        "Revisión general": "#FFBD45",
        "Revisión específica": "#3DD56D",
        "Ecografías": "#6C9DFF",
        "Limpieza bucal": "#FFD700",
        "Extracción de piezas dentales": "#FF69B4",
        "Cirugía": "#FF6347",
    }
    color = treatment_colors.get(tratamiento, "#FFFFFF")  # Default color is white

    cita_guardada = save_cita(nueva_cita)
    if cita_guardada:
        st.session_state["events"].append({
            "id": str(cita_guardada["id"]),  # Cambiado de _id a id
            "title": f"{tratamiento} - {cliente_id}",
            "start": fecha_inicio,
            "end": fecha_fin,
            "color": "#FF6347",
            "sub_treatments": subtratamientos
        })
        st.success(f"Cita registrada para el cliente {cliente_id} con tratamiento {tratamiento}.")
        return True
    return False


def save_dragged_event(event_id, new_start, new_end):
    """Actualiza las fechas de una cita arrastrada."""
    try:
        # Convertir nuevos tiempos a datetime sin zona horaria
        new_start_dt = datetime.fromisoformat(new_start).replace(tzinfo=None)
        new_end_dt = datetime.fromisoformat(new_end).replace(tzinfo=None)

        # Crear una lista de eventos para verificar conflictos (excluyendo el evento actual)
        conflict_events = [event for event in st.session_state["events"] if event['id'] != event_id]

        # Verificar conflictos antes de actualizar
        for event in conflict_events:
            event_start = datetime.fromisoformat(event['start']).replace(tzinfo=None)
            event_end = datetime.fromisoformat(event['end']).replace(tzinfo=None)

            # Verificar si hay solape
            if new_start_dt < event_end and new_end_dt > event_start:
                st.error("Error: No se puede mover la cita. El nuevo horario está ocupado.")
                return False

        # Actualizar las fechas en la API
        update_data = {
            "fecha_inicio": new_start,
            "fecha_fin": new_end,
        }
        response = requests.put(f"{API_URL}/citas/{event_id}", json=update_data)

        if response.status_code == 200:
            # Actualizar localmente
            for event in st.session_state["events"]:
                if event["id"] == event_id:
                    event["start"] = new_start
                    event["end"] = new_end
                    break
            st.toast("Evento actualizado correctamente", icon="✅")
            return True
        else:
            st.error(f"Error al actualizar la cita en el servidor. Respuesta: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error al guardar el evento: {e}")
        return False

        
def check_appointment_conflict(new_start, new_end, events):
    """Verifica si una nueva cita entra en conflicto con las citas existentes."""
    try:
        new_start_dt = datetime.fromisoformat(new_start).replace(tzinfo=None)
        new_end_dt = datetime.fromisoformat(new_end).replace(tzinfo=None)

        for event in events:
            event_start = datetime.fromisoformat(event["start"]).replace(tzinfo=None)
            event_end = datetime.fromisoformat(event["end"]).replace(tzinfo=None)

            if new_start_dt < event_end and new_end_dt > event_start:
                return True  # Conflicto encontrado
        return False  # No hay conflictos
    except Exception as e:
        st.error(f"Error al verificar conflictos: {e}")
        return True


# Función para actualizar un evento en la lista de eventos
def update_event(event_id, new_start, new_end):
    """Actualiza un evento existente en la lista de eventos y en el archivo citas.json."""
    # Buscar y actualizar el evento en la lista de eventos de la sesión
    for event in st.session_state["events"]:
        if event["id"] == event_id:
            event["start"] = new_start
            event["end"] = new_end
            break
    
    # Guardar los eventos actualizados en citas.json
    with open("citas.json", "w") as file:
        json.dump(st.session_state["events"], file, indent=4)
    
# Función para mostrar el popup y registrar la cita
@st.dialog("Registrar cita")
def popup():
    """Mostrar el formulario en un popup."""
    start_time = st.session_state.get("time_inicial")
    end_time = st.session_state.get("time_final")

    if not start_time or not end_time:
        st.error("No se ha seleccionado una franja horaria válida.")
        return

    st.write(f"Registrar cita desde {start_time} hasta {end_time}")

    # Formulario para registrar la cita
    cliente_id = st.text_input("ID del cliente:")
    mascota_id = st.text_input("ID de la mascota (opcional):")

    # Selección de tratamiento principal
    main_treatment = st.selectbox(
        "Seleccione un tratamiento principal:",
        list(treatments.keys())
    )

    # Actualizar el estado del tratamiento principal y limpiar subtratamientos si se cambia
    if main_treatment != st.session_state["main_treatment"]:
        st.session_state["main_treatment"] = main_treatment
        st.session_state["selected_sub_treatments"] = []  # Limpiar subtratamientos seleccionados

    # Subtratamientos dinámicos
    sub_treatments_options = treatments[st.session_state["main_treatment"]]
    selected_sub_treatments = st.multiselect(
        f"Seleccione opciones específicas para {st.session_state['main_treatment']}:",
        sub_treatments_options,
        default=st.session_state["selected_sub_treatments"]
    )
    st.session_state["selected_sub_treatments"] = selected_sub_treatments

    # Botón para guardar la cita
    if st.button("Guardar cita"):
        if not cliente_id or not main_treatment:
            st.error("Por favor, complete los campos obligatorios.")
        else:
            # Registrar la cita en el calendario
            success = register_appointment(
                cliente_id=cliente_id,
                mascota_id=mascota_id,
                fecha_inicio=start_time,
                fecha_fin=end_time,
                tratamiento=main_treatment,
                subtratamientos=selected_sub_treatments,
            )
           
# Función para manejar el clic en un evento y mostrar las opciones
def event_options_popup(event_data):
    """Muestra un popup con opciones al hacer clic en un evento."""
    # Extraer datos del evento clickeado
    event_id = event_data.get("event", {}).get("id")
    evento_title = event_data.get("event", {}).get("title", "Título no disponible")
    cliente_id = event_data.get("event", {}).get("extendedProps", {}).get("cliente_id", "ID no disponible")

    # Verificar si se ha encontrado un evento válido
    if not event_id:
        st.error("No se encontró información válida para este evento.")
        return

    # Mostrar las opciones
    st.subheader(f"Opciones para el evento: {evento_title}")

    # Opción de facturación
    with st.expander("Facturación"):
        st.write(f"**Título del evento:** {evento_title}")
        st.write(f"**ID del cliente:** {cliente_id}")

        # Entrada para el importe
        importe = st.number_input("Ingrese el importe de la factura:", min_value=0.0, format="%.2f", key=f"factura_importe_{event_id}")

        # Al pulsar este botón, se crea la factura directamente en la base de datos
        if st.button("Registrar Factura", key=f"registrar_factura_{event_id}"):
            factura = {
                "cita_id": event_id,
                "precio": importe
            }

            response = requests.post(f"{API_URL}/facturas/", json=factura)

            if response.status_code == 200:
                st.success(f"Factura registrada correctamente con un importe de {importe:.2f}.")
            else:
                st.error("Error al registrar la factura en la base de datos.")

    # Opción de eliminar cita
    if st.button("Eliminar cita"):
        # Eliminar la cita seleccionada
        delete_cita(event_id) # Actualizar en la base de datos
        st.session_state["events"] = [
            event for event in st.session_state["events"] if event["id"] != event_id
        ]
          

        st.success(f"Cita '{evento_title}' eliminada correctamente.")

# Configuración del calendario
calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "selectable": "true",
    "initialDate": "2024-12-08",
    "initialView": "timeGridWeek",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "timeGridWeek,dayGridMonth",
    }
}

# Renderizar calendario
state = calendar(
    events=st.session_state["events"],
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key="timegrid",
)

# Capturar selección de franja horaria
if state.get("select"):
    st.session_state["time_inicial"] = state["select"]["start"]
    st.session_state["time_final"] = state["select"]["end"]
    popup()
    
# Detectar clic en un evento del calendario
if state.get("eventClick"):
    event_options_popup(state["eventClick"])
    
# Encabezado
st.header("Citas registradas")

# Verificar si hay eventos
if not st.session_state["events"]:
    st.info("No hay citas registradas.")
else:
    # Convertir los eventos a un DataFrame para visualización
    citas_data = []
    for event in st.session_state["events"]:
        # Dividir la fecha y la hora
        start_datetime = datetime.fromisoformat(event["start"]).replace(tzinfo=None)
        end_datetime = datetime.fromisoformat(event["end"]).replace(tzinfo=None)

        citas_data.append({
            "ID Cliente": event.get("cliente_id", "Desconocido"),
            "Tratamiento": event.get("title", "No especificado"),
            "Subtratamientos": ", ".join(event.get("sub_treatments", [])) if event.get("sub_treatments") else "Ninguno",
            "Fecha": start_datetime.date().isoformat(),
            "Hora Inicio": start_datetime.time().strftime("%H:%M"),
            "Hora Fin": end_datetime.time().strftime("%H:%M"),
        })

    citas_df = pd.DataFrame(citas_data)


    # Mostrar la tabla
    st.dataframe(
        citas_df,
        use_container_width=True,  # Hace que la tabla ocupe todo el ancho disponible
        height=400  # Altura de la tabla
    )
    
# Código para detectar el arrastre de eventos
if state.get("eventDrop"):
    dropped_event = state["eventDrop"]
    event_id = dropped_event.get("event", {}).get("id")
    new_start = dropped_event.get("event", {}).get("start")
    new_end = dropped_event.get("event", {}).get("end")
    
    if event_id and new_start and new_end:
        # Guardar el evento arrastrado
        success = save_dragged_event(
            event_id, 
            new_start.isoformat(), 
            new_end.isoformat()
        )
        
        # Si el guardado falla, revertir el movimiento
        if not success:
            st.rerun()