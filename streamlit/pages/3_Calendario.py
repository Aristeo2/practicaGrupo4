import streamlit as st
from streamlit_calendar import calendar
import requests

# Configuración de la API FastAPI
API_URL = "http://fastapi:8000"

# Inicializar el estado
if "events" not in st.session_state:
    st.session_state["events"] = []

# Título de la aplicación
st.title("Gestión de Citas con Calendario 📆")

# Función para cargar citas desde FastAPI
def load_citas():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        citas = response.json()
        events = [
            {
                "title": cita["animal_name"],
                "start": cita["fecha_inicio"],
                "end": cita["fecha_fin"],
                "color": "#FF6C6C",
                "resourceId": cita["cliente_id"],
            }
            for cita in citas
        ]
        return events
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar citas: {e}")
        return []

# Función para enviar una nueva cita al backend
def send_cita(data):
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error al registrar la cita: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API: {e}")
        return False

# Cargar las citas al inicio
if not st.session_state["events"]:
    st.session_state["events"] = load_citas()

# Opciones del calendario
calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "selectable": "true",
    "initialDate": "2023-07-01",
    "initialView": "timeGridWeek",
}

# Mostrar el calendario
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

# Función para mostrar el popup y registrar una cita
def popup():
    """Mostrar formulario para registrar una nueva cita."""
    start_time = st.session_state.get("time_inicial")
    end_time = st.session_state.get("time_final")

    if not start_time or not end_time:
        st.error("No se ha seleccionado una franja horaria válida.")
        return

    st.write(f"Registrar cita desde {start_time} hasta {end_time}")

    with st.form("cita_form"):
        owner_name = st.text_input("Nombre del dueño:")
        animal_name = st.text_input("Nombre del animal:")
        treatment = st.text_input("Tratamiento:")
        subtratamientos = st.text_area("Subtratamientos (separados por comas):")
        submitted = st.form_submit_button("Registrar Cita")

        if submitted:
            cita = {
                "owner_name": owner_name,
                "animal_name": animal_name,
                "treatment": treatment,
                "subtratamientos": [s.strip() for s in subtratamientos.split(",") if s],
                "fecha_inicio": start_time,
                "fecha_fin": end_time,
                "cliente_id": "cliente1",  # Ajustar con el cliente real si lo tienes
            }
            if send_cita(cita):
                st.success("Cita registrada con éxito.")
                st.session_state["events"].append({
                    "title": animal_name,
                    "start": start_time,
                    "end": end_time,
                    "color": "#FF6C6C",
                })

# Manejar eventos de selección en el calendario
if state.get("select"):
    st.session_state["time_inicial"] = state["select"]["start"]
    st.session_state["time_final"] = state["select"]["end"]
    popup()

# Manejar cambios en eventos del calendario
if state.get("eventChange"):
    data = state["eventChange"]["event"]
    st.success("Cita modificada con éxito.")
    # Aquí puedes agregar la lógica para actualizar la cita en la API.
