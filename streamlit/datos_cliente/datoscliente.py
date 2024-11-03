import re

class Verificar_Cliente():
    def __init__(self, nombre, dni, direccion, telefono, email):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    def verificar_nombre(self):
        """Verifica que el nombre solo contenga letras y espacios, y tenga una longitud válida."""
        if len(self.nombre) < 2 or len(self.nombre) > 50:
            return False, "El nombre debe tener entre 2 y 50 caracteres."
        if not all(x.isalpha() or x.isspace() for x in self.nombre):
            return False, "El nombre solo puede contener letras y espacios."
        return True, "Nombre válido."

    def verificar_dni(self):
        """Verifica que el DNI tenga 8 dígitos y, opcionalmente, una letra al final."""
        # Patrón: 8 dígitos opcionalmente seguidos de una letra
        patron_dni = r"^\d{8}[A-Za-z]?$"
        if not re.match(patron_dni, self.dni):
            return False, "Formato de DNI no válido."
        return True, "DNI válido."

    def verificar_direccion(self):
        """Verifica que la dirección tenga entre 5 y 100 caracteres."""
        if len(self.direccion) < 5 or len(self.direccion) > 100:
            return False, "La dirección debe tener entre 5 y 100 caracteres."
        return True, "Dirección válida."

    def verificar_telefono(self):
        """Verifica que el número de teléfono solo contenga dígitos y tenga entre 7 y 15 caracteres."""
        if not self.telefono.isdigit() or not (7 <= len(self.telefono) <= 15):
            return False, "El teléfono debe contener solo dígitos y tener entre 7 y 15 caracteres."
        return True, "Teléfono válido."

    def verificar_email(self):
        """Verifica que el email tenga un formato válido."""
        # Expresión regular para validar el formato de un correo electrónico
        patron_email = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        if not re.match(patron_email, self.email):
            return False, "Formato de correo electrónico no válido."
        return True, "Correo electrónico válido."

    def verificar_formulario(self):
        """Verifica todos los campos del formulario y devuelve los resultados."""
        resultados = {
            "nombre": self.verificar_nombre(),
            "dni": self.verificar_dni(),
            "direccion": self.verificar_direccion(),
            "telefono": self.verificar_telefono(),
            "email": self.verificar_email()
        }
        return resultados

cliente = Verificar_Cliente(
    "Juan Pérez",
    "12345678R",
    "Calle Falsa 123, Ciudad",
    "123456789",
    "juan.perez@example.com"
)

resultados = cliente.verificar_formulario()

for campo, (valido, mensaje) in resultados.items():
    print(f"{campo.capitalize()}: {'✔' if valido else '✘'} - {mensaje}")