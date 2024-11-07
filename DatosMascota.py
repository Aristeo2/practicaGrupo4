import re
from datetime import datetime

class VerificarMascota:
    
    @staticmethod
    def nombre(nombre):
        
        if not nombre:
            return False
        
        
        if not all(c.isalpha() or c.isspace() for c in nombre):
            return False
        
        
        if not nombre[0].isupper():
            return False
        
        
        return True
    
    def tipo(animal):
        
        if animal in ["Perro", "Gato"]:
            return True
        else:
            return False
    
   
    def raza(raza):
     
        if not raza:
            return False
        
        
        if len(raza) >= 20:
            return False
        
        
        if not all(c.isalpha() or c.isspace() for c in raza):
            return False
        
       
        if not raza[0].isupper():
            return False
        
        
        return True
    
    @staticmethod
    def fecha_nacimiento(fecha):
        
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True  
        except ValueError:
            return False  
    
    @staticmethod
    def patologias(patologia):
        # Verifica que la patología no esté vacía
        if not patologia:
            return False
        # Verifica que la patología no contenga números ni caracteres especiales
        if not all(c.isalpha() or c.isspace() for c in patologia):
            return False
        # Verifica que la primera letra de la patología sea mayúscula
        if not patologia[0].isupper():
            return False
        return True
#Como los filtros aplicados al nombre del perro son los mismos que queremos
#usar para el nombre del dueño recurrimos a lo hecho antes 
#NO PONER TRUE TRUE YA ESTA EN EL METODO NOMBRE
    @staticmethod
    def dueño(dueño):
        return VerificarMascota.nombre(dueño) 