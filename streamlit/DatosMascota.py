import re
from datetime import datetime

class VerificarMascota:
    
    @staticmethod
    def nombre(nombre):
        """Valida el nombre de la mascota o del dueño."""
        if not nombre:
            return False
        
        # Permitir letras, espacios y caracteres especiales como tildes (á, é, í, ó, ú)
        if not all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚ" for c in nombre):
            return False
        
        # Verifica que el nombre empiece con una letra mayúscula
        if not nombre[0].isupper():
            return False
        
        return True
    
    @staticmethod
    def tipo(animal):
        """Valida si el tipo de animal es 'Perro' o 'Gato'."""
        if animal in ["Perro", "Gato"]:
            return True
        else:
            return False
    
    @staticmethod
    def raza(raza):
        """Valida la raza de la mascota."""
        if not raza:
            return False
        
        # Limitar la longitud de la raza a 20 caracteres
        if len(raza) >= 20:
            return False
        
        # Permitir letras, espacios y caracteres especiales como tildes (á, é, í, ó, ú)
        if not all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚ" for c in raza):
            return False
        
        # Verifica que la raza empiece con una letra mayúscula
        if not raza[0].isupper():
            return False
        
        return True
    
    @staticmethod
    def fecha_nacimiento(fecha):
        """Valida la fecha de nacimiento de la mascota."""
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True  
        except ValueError:
            return False  
    
    @staticmethod
    def patologias(patologia):
        """Valida las patologías de la mascota."""
        # Verifica que la patología no esté vacía
        if not patologia:
            return False
        
        # Permitir letras, espacios y caracteres especiales como tildes (á, é, í, ó, ú)
        if not all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚ" for c in patologia):
            return False
        
        # Verifica que la primera letra de la patología sea mayúscula
        if not patologia[0].isupper():
            return False
        
        return True

    @staticmethod
    def dueño(dueño):
        """Valida el nombre del dueño de la mascota, similar a la validación de nombre."""
        return VerificarMascota.nombre(dueño)
