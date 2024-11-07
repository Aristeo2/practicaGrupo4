import streamlit as st
import re

class Verificar_Cliente:
        
    @staticmethod
    def verificar_nombre(nombre):
        """Verifica que el nombre solo contenga letras y espacios, y tenga una longitud válida."""
        if len(nombre) < 2 or len(nombre) > 50:
            return False, "El nombre debe tener entre 2 y 50 caracteres."
        if not all(x.isalpha() or x.isspace() for x in nombre):
            return False, "El nombre solo puede contener letras y espacios."
        return True, "Nombre válido."

    @staticmethod
    def verificar_dni(dni):
        """Verifica que el DNI tenga 8 dígitos y, opcionalmente, una letra al final."""
        # Patrón: 8 dígitos opcionalmente seguidos de una letra
        patron_dni = r"^\d{8}[A-Za-z]?$"
        if not re.match(patron_dni, dni):
            return False, "Formato de DNI no válido."
        return True, "DNI válido."

    @staticmethod
    def verificar_direccion(direccion):
        """Verifica que la dirección tenga entre 5 y 100 caracteres."""
        if len(direccion) < 5 or len(direccion) > 100:
            return False, "La dirección debe tener entre 5 y 100 caracteres."
        return True, "Dirección válida."

    @staticmethod
    def verificar_telefono(telefono):
        """Verifica que el número de teléfono solo contenga dígitos y tenga entre 7 y 15 caracteres."""
        if not telefono.isdigit() or not (7 <= len(telefono) <= 15):
            return False, "El teléfono debe contener solo dígitos y tener entre 7 y 15 caracteres."
        return True, "Teléfono válido."

    @staticmethod
    def verificar_email(email):
        """Verifica que el email tenga un formato válido."""
        # Expresión regular para validar el formato de un correo electrónico
        patron_email = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        if not re.match(patron_email, email):
            return False, "Formato de correo electrónico no válido."
        return True, "Correo electrónico válido."

    @staticmethod
    def verificar_formulario(nombre, dni, direccion, telefono, email):
        """Verifica todos los campos del formulario y devuelve los resultados."""
        resultados = {
            "nombre": Verificar_Cliente.verificar_nombre(nombre),
            "dni": Verificar_Cliente.verificar_dni(dni),
            "direccion": Verificar_Cliente.verificar_direccion(direccion),
            "telefono": Verificar_Cliente.verificar_telefono(telefono),
            "email": Verificar_Cliente.verificar_email(email)
        }
        return resultados

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
    if nombre and dni and direccion and telefono and email:
        st.success("¡Dueño registrado exitosamente!")
        st.write("Información del Dueño:")
        st.write(f"**Nombre:** {nombre}")
        st.write(f"**DNI:** {dni}")
        st.write(f"**Dirección:** {direccion}")
        st.write(f"**Teléfono:** {telefono}")
        st.write(f"**Correo Electrónico:** {email}")
    else:
        st.error("Por favor, complete todos los campos del formulario.")
