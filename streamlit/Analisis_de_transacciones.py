import streamlit as st
import time
import importlib

# Configuración de la página
st.set_page_config(
    page_title="Clínica Veterinaria Paws & Care",
    layout="wide",
    page_icon="🐾"
)

# Estilos personalizados para la página
st.markdown(
    """
    <style>
    .main-title {
        font-size: 3em;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.5em;
        color: #555;
        text-align: center;
        margin-bottom: 40px;
    }
    .sidebar .sidebar-content {
        background-color: #f9f9f9;
        padding: 20px;
    }
    .footer {
        font-size: 0.9em;
        color: #999;
        text-align: center;
        margin-top: 40px;
    }
    .service-box {
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #fefefe;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .service-box h3 {
        color: #4CAF50;
    }
    .sidebar .sidebar-content {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Arial', sans-serif;
    }
    .sidebar .sidebar-content h1 {
        color: #4CAF50;
        font-size: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Imagen y título principal
st.image("logo.jpg", use_column_width="always")
st.markdown('<div class="main-title">¡Bienvenidos a Paws & Care! 🐾</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Cuidando a tus amigos peludos con amor y dedicación.</div>', unsafe_allow_html=True)

# Simulación de carga
placeholder = st.empty()
with placeholder:
    for seconds in range(3):
        placeholder.write(f"⏳ {seconds + 1} segundos - Preparando nuestra clínica virtual...")
        time.sleep(1)
placeholder.empty()

# Servicios principales
st.write("## Nuestros Servicios Principales")
cols = st.columns(3)

with cols[0]:
    st.markdown('<div class="service-box"><h3>Consultas Médicas</h3><p>Atención personalizada para el cuidado de la salud de tus mascotas.</p></div>', unsafe_allow_html=True)

with cols[1]:
    st.markdown('<div class="service-box"><h3>Vacunación</h3><p>Protege a tus amigos peludos con nuestro plan completo de vacunas.</p></div>', unsafe_allow_html=True)

with cols[2]:
    st.markdown('<div class="service-box"><h3>Estética y Baños</h3><p>Mantén a tus mascotas limpias y felices con nuestros servicios de grooming.</p></div>', unsafe_allow_html=True)

# Información de contacto
st.write("### Contáctanos")
st.write("📍 **Dirección:** Calle Siempreviva 123, Springfield")
st.write("📞 **Teléfono:** +1 234 567 890")
st.write("📧 **Email:** contacto@pawsandcare.com")
