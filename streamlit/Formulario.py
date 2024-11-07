import streamlit as st
from datos_cliente.datoscliente import Verificar_Cliente

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
        st.success("¡Dueño registrado exitosamente!")
        st.write("Información del Dueño:")
        st.write(f"**Nombre:** {nombre}")
        st.write(f"**DNI:** {dni}")
        st.write(f"**Dirección:** {direccion}")
        st.write(f"**Teléfono:** {telefono}")
        st.write(f"**Correo Electrónico:** {email}")