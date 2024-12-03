import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import requests
import uuid

# URL base de la API
API_URL = "http://fastapi:8000"

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

# Funciones para interactuar con la API
def create_citas(cita):
    response = requests.post(f"{API_URL}/citas", json=cita)
    return response.json() if response.status_code == 200 else None

def get_citas():
    response = requests.get(f"{API_URL}/citas/")
    return response.json() if response.status_code == 200 else []

# Cargar citas desde la API al inicio
if "events" not in st.session_state:
    citas = get_citas()
    st.session_state["events"] = [
        {
            "id": cita["id"],
            "title": cita["title"],
            "start": cita["start"],
            "end": cita["end"],
            "color": cita.get("color", "#FFFFFF"),  # Color opcional
            "cliente_id": cita["cliente_id"],
            "mascota_id": cita.get("mascota_id", ""),
            "sub_treatments": cita.get("sub_treatments", []),
        }
        for cita in citas
    ]

if "main_treatment" not in st.session_state:
    st.session_state["main_treatment"] = list(treatments.keys())[0]

if "selected_sub_treatments" not in st.session_state:
    st.session_state["selected_sub_treatments"] = []

# Función para registrar una cita usando la API
def register_appointment(cliente_id, mascota_id, fecha_inicio, fecha_fin, tratamiento, subtratamientos):
    """Registrar la cita a través de la API."""
    # Crear el cuerpo de la cita
    cita = {
        "id": str(uuid.uuid4()),  # Generar un ID único para la cita
        "title": f"{tratamiento} - {cliente_id}",
        "start": fecha_inicio.isoformat(),
        "end": fecha_fin.isoformat(),
        "color": treatment_colors.get(tratamiento, "#FFFFFF"),  # Color basado en el tratamiento
        "cliente_id": cliente_id,
        "mascota_id": mascota_id,
        "sub_treatments": subtratamientos,
    }

    # Enviar cita a la API
    response = create_citas(cita)
    if response:
        st.session_state["events"].append(cita)
        st.success(f"Cita registrada para el cliente {cliente_id} con tratamiento {tratamiento}.")
    else:
        st.error("Error al registrar la cita. Verifique los datos e intente nuevamente.")

# Configuración de colores para tratamientos
treatment_colors = {
    "Análisis de sangre y hormonales": "#FF6C6C",
    "Revisión general": "#FFBD45",
    "Revisión específica": "#3DD56D",
    "Ecografías": "#6C9DFF",
    "Limpieza bucal": "#FFD700",
    "Extracción de piezas dentales": "#FF69B4",
    "Cirugía": "#FF6347",
}

# Función para mostrar el popup y registrar la cita
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
            # Registrar la cita a través de la API
            register_appointment(
                cliente_id=cliente_id,
                mascota_id=mascota_id,
                fecha_inicio=start_time,
                fecha_fin=end_time,
                tratamiento=main_treatment,
                subtratamientos=selected_sub_treatments,
            )


# Configuración del calendario
calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "selectable": "true",
    "initialDate": "2023-07-01",
    "initialView": "timeGridWeek",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "timeGridWeek,dayGridMonth",
    },
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

# Mostrar citas registradas
st.header("Citas registradas:")
for event in st.session_state["events"]:
    st.write(
        f"- **ID Cliente:** {event['cliente_id']} | **Tratamiento:** {event['title']}\n"
        f"  Subtratamientos: {', '.join(event['sub_treatments']) if event['sub_treatments'] else 'Ninguno'}\n"
        f"  Horario: {event['start']} - {event['end']}"
    )