import streamlit as st

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
    if nombre and dni and direccion and telefono and correo:
        st.success("¡Dueño registrado exitosamente!")
        st.write("Información del Dueño:")
        st.write(f"**Nombre:** {nombre}")
        st.write(f"**DNI:** {dni}")
        st.write(f"**Dirección:** {direccion}")
        st.write(f"**Teléfono:** {telefono}")
        st.write(f"**Correo Electrónico:** {correo}")
    else:
        st.error("Por favor, complete todos los campos del formulario.")
