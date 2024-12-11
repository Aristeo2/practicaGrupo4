import re
import logging
from datetime import datetime

# Configuración del logger
logging.basicConfig(
    filename='errores_mascotas.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class VerificarMascota:

    @staticmethod
    def nombre(nombre):
        """Valida el nombre de la mascota."""
        if not nombre:
            logging.error("Nombre vacío.")
            return False

        patron_nombre = r"^[A-Za-zÁÉÍÓÚáéíóúÑñüÜ\-' ]+$"
        if not re.match(patron_nombre, nombre):
            logging.error(f"Nombre inválido: {nombre}.")
            return False

        if not nombre[0].isupper():
            logging.error(f"El nombre no empieza con mayúscula: {nombre}.")
            return False

        return True

    @staticmethod
    def tipo(animal):
        """Valida si el tipo de animal es 'Perro' o 'Gato'."""
        if animal in ["Perro", "Gato"]:
            return True
        else:
            logging.error(f"Tipo de animal inválido: {animal}.")
            return False

    @staticmethod
    def raza(raza):
        """Valida la raza de la mascota."""
        if not raza:
            logging.error("Raza vacía.")
            return False

        if len(raza) > 20:
            logging.error(f"Raza demasiado larga: {raza}.")
            return False

        patron_raza = r"^[A-Za-zÁÉÍÓÚáéíóúÑñüÜ\-' ]+$"
        if not re.match(patron_raza, raza):
            logging.error(f"Raza inválida: {raza}.")
            return False

        if not raza[0].isupper():
            logging.error(f"La raza no empieza con mayúscula: {raza}.")
            return False

        return True

    @staticmethod
    def fecha_nacimiento(fecha):
        """Valida la fecha de nacimiento de la mascota."""
        try:
            fecha_nacimiento = datetime.strptime(fecha, "%d/%m/%Y")
            if fecha_nacimiento > datetime.now():
                logging.error(f"Fecha futura: {fecha}.")
                return False
            return True
        except ValueError:
            logging.error(f"Fecha inválida: {fecha}.")
            return False

    @staticmethod
    def patologias(patologia):
        """Valida las patologías de la mascota."""
        if not patologia:
            logging.error("Patología vacía.")
            return False

        patron_patologia = r"^[A-Za-zÁÉÍÓÚáéíóúÑñüÜ\-' ]+$"
        if not re.match(patron_patologia, patologia):
            logging.error(f"Patología inválida: {patologia}.")
            return False

        if not patologia[0].isupper():
            logging.error(f"La patología no empieza con mayúscula: {patologia}.")
            return False

        return True

    @staticmethod
    def dueño(dueño):
        """Valida el nombre del dueño de la mascota."""
        return VerificarMascota.nombre(dueño)
