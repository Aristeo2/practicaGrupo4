import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta

# Diccionario para tratamientos y subtratamientos
treatments = {
    "Análisis de sangre y hormonales": ["Vacunación", "Desparasitación"],
    "Revisión general": [],
    "Revisión específica": ["Cardiología", "Cutánea", "Broncológica"],
    "Ecografías": [],
    "Limpieza bucal": [],
    "Extracción de piezas dentales": [],
    "Cirugía": ["Castración", "Abdominal", "Cardíaca", "Articular y ósea", "Hernias"]
}

# Base de datos simulada para las citas
appointments = []

def main():
    st.title("Gestión de citas - Clínica Veterinaria")

    # Página principal
    page = st.sidebar.radio("Seleccione una opción", ["Calendario", "Crear Cita"])

    if page == "Calendario":
        show_calendar()
    elif page == "Crear Cita":
        create_appointment()

def show_calendar():
    """Muestra el calendario donde se puede seleccionar un día para ver las citas."""
    st.header("Calendario de citas")

    # Usamos streamlit_calendar para mostrar un calendario interactivo
    selected_date = calendar()

    if selected_date:
        st.write(f"Seleccionaste el día: {selected_date}")

        # Mostrar citas para el día seleccionado
        daily_appointments = [appt for appt in appointments if appt["start_date"] == selected_date]

        if daily_appointments:
            st.subheader(f"Citas para el {selected_date}:")
            for appt in daily_appointments:
                st.write(
                    f"- **{appt['animal_name']}** ({appt['owner_name']})\n"
                    f"  Tratamiento: {appt['treatment']}\n"
                    f"  Subtratamientos: {', '.join(appt['sub_treatments']) if appt['sub_treatments'] else 'Ninguno'}\n"
                    f"  Hora: {appt['start_time']} - {appt['end_time']}"
                )
        else:
            st.write("No hay citas para este día.")

def create_appointment():
    """Formulario para crear una nueva cita."""
    st.header("Crear nueva cita")

    # Formulario de cita
    owner_name = st.text_input("Nombre del dueño:")
    animal_name = st.text_input("Nombre del animal:")

    # Selección de tratamiento principal
    main_treatment = st.selectbox("Seleccione un tratamiento principal:", list(treatments.keys()))

    # Subtratamientos dinámicos basados en el tratamiento seleccionado
    sub_treatments = []
    if treatments[main_treatment]:
        sub_treatments = st.multiselect(
            f"Seleccione opciones específicas para {main_treatment}:",
            treatments[main_treatment]
        )

    # Usamos streamlit_calendar para seleccionar la fecha de inicio
    start_date = st.date_input("Fecha de inicio:")
    
    # Generamos las opciones de horas entre 8:00 AM y 10:00 PM en intervalos de 30 minutos
    hours = [f"{h:02d}:{m:02d}" for h in range(8, 23) for m in [0, 30]]  # 08:00, 08:30, 09:00, 09:30, etc.

    # Usamos selectbox para elegir la hora
    start_time = st.selectbox("Hora de inicio:", hours)

    # Usamos la misma hora predeterminada para la fecha de fin
    end_date = st.date_input("Fecha de fin:", start_date)

    # Usamos selectbox para elegir la hora de fin (mismo rango)
    end_time = st.selectbox("Hora de fin:", hours)

    # Validación para asegurarse de que la hora de fin sea posterior a la hora de inicio
    if end_time <= start_time:
        st.error("La hora de fin debe ser posterior a la hora de inicio y no puede ser igual.")
    
    # Botón para guardar la cita
    if st.button("Guardar cita"):
        if not owner_name or not animal_name:
            st.error("Por favor, complete todos los campos obligatorios.")
        else:
            appointment = {
                "owner_name": owner_name,
                "animal_name": animal_name,
                "treatment": main_treatment,
                "sub_treatments": sub_treatments,
                "start_date": start_date,
                "start_time": start_time,
                "end_date": end_date,
                "end_time": end_time
            }
            appointments.append(appointment)
            st.success(f"Cita para {animal_name} creada con éxito.")
            st.json(appointment)

if __name__ == "__main__":
    main()