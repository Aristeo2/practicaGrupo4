import re
import logging

# Configuración básica del logger
logging.basicConfig(
    filename='errores.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Verificar_Cliente:

    @staticmethod
    def verificar_nombre(nombre):
        """Verifica que el nombre permita letras con tildes, guiones, apóstrofes y espacios."""
        if len(nombre) < 2 or len(nombre) > 50:
            return False, "El nombre debe tener entre 2 y 50 caracteres."
        # Permitir letras con tildes, guiones y apóstrofes
        patron_nombre = r"^[A-Za-zÁÉÍÓÚáéíóúÑñüÜ\-' ]+$"
        if not re.match(patron_nombre, nombre):
            return False, "El nombre solo puede contener letras, espacios, guiones y apóstrofes."
        return True, "Nombre válido."

    @staticmethod
    def verificar_dni(dni):
        """Verifica que el DNI tenga 8 dígitos y opcionalmente una letra al final."""
        patron_dni = r"^\d{8}[A-Za-z]?$"
        if not re.match(patron_dni, dni):
            return False, "Formato de DNI no válido."
        return True, "DNI válido."

    @staticmethod
    def verificar_direccion(direccion):
        """Verifica que la dirección tenga entre 5 y 100 caracteres y no contenga caracteres especiales no permitidos."""
        if len(direccion) < 5 or len(direccion) > 100:
            return False, "La dirección debe tener entre 5 y 100 caracteres."
        if re.search(r"[@#*]", direccion):
            return False, "La dirección no puede contener caracteres especiales como @, # o *."
        return True, "Dirección válida."

    @staticmethod
    def verificar_telefono(telefono):
        """Verifica que el número de teléfono solo contenga dígitos y tenga entre 7 y 15 caracteres."""
        if not telefono.isdigit() or not (7 <= len(telefono) <= 15):
            return False, "El teléfono debe contener solo dígitos y tener entre 7 y 15 caracteres. No se permiten letras ni caracteres especiales."
        return True, "Teléfono válido."

    @staticmethod
    def verificar_email(email):
        """Verifica que el email tenga un formato válido."""
        patron_email = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        if not re.match(patron_email, email):
            return False, "Formato de correo electrónico no válido."
        return True, "Correo electrónico válido."

    @staticmethod
    def verificar_formulario(nombre, dni, direccion, telefono, email):
        """Verifica todos los campos del formulario y devuelve los resultados."""
        try:
            resultados = {
                "nombre": Verificar_Cliente.verificar_nombre(nombre),
                "dni": Verificar_Cliente.verificar_dni(dni),
                "direccion": Verificar_Cliente.verificar_direccion(direccion),
                "telefono": Verificar_Cliente.verificar_telefono(telefono),
                "email": Verificar_Cliente.verificar_email(email)
            }
            return resultados
        except Exception as e:
            logging.error(f"Error al verificar formulario: {e}")
            return {
                "error": (False, "Error interno al procesar el formulario.")
            }
