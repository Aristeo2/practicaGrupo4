import unittest
from datoscliente import Verificar_Cliente 

class TestVerificar_Cliente(unittest.TestCase):

    def setUp(self):
        # Atributos generales para usar en las pruebas, cambiando los valores específicos
        self.nombre_valido = "Nombre Ejemplo"
        self.nombre_invalido = "N"
        self.dni_valido = "87654321B"
        self.dni_invalido = "12345"
        self.direccion_valida = "Direccion Completa Ejemplo 123"
        self.direccion_invalida = "Dir"
        self.telefono_valido = "987654321"
        self.telefono_invalido = "1234"
        self.email_valido = "correo@ejemplo.com"
        self.email_invalido = "correoexample.com"

    def test_verificar_nombre(self):
        # Prueba de método sin valores específicos en el código de la prueba
        cliente = Verificar_Cliente(self.nombre_valido, self.dni_valido, self.direccion_valida, self.telefono_valido, self.email_valido)
        resultado_valido = cliente.verificar_nombre()
        self.assertTrue(resultado_valido[0])  # El resultado debe ser True para un nombre válido
        
        cliente.nombre = self.nombre_invalido
        resultado_invalido = cliente.verificar_nombre()
        self.assertFalse(resultado_invalido[0])  # El resultado debe ser False para un nombre inválido

    def test_verificar_dni(self):
        cliente = Verificar_Cliente(self.nombre_valido, self.dni_valido, self.direccion_valida, self.telefono_valido, self.email_valido)
        resultado_valido = cliente.verificar_dni()
        self.assertTrue(resultado_valido[0])  # DNI válido
        
        cliente.dni = self.dni_invalido
        resultado_invalido = cliente.verificar_dni()
        self.assertFalse(resultado_invalido[0])  # DNI inválido

    def test_verificar_direccion(self):
        cliente = Verificar_Cliente(self.nombre_valido, self.dni_valido, self.direccion_valida, self.telefono_valido, self.email_valido)
        resultado_valido = cliente.verificar_direccion()
        self.assertTrue(resultado_valido[0])  # Dirección válida
        
        cliente.direccion = self.direccion_invalida
        resultado_invalido = cliente.verificar_direccion()
        self.assertFalse(resultado_invalido[0])  # Dirección inválida

    def test_verificar_telefono(self):
        cliente = Verificar_Cliente(self.nombre_valido, self.dni_valido, self.direccion_valida, self.telefono_valido, self.email_valido)
        resultado_valido = cliente.verificar_telefono()
        self.assertTrue(resultado_valido[0])  # Teléfono válido
        
        cliente.telefono = self.telefono_invalido
        resultado_invalido = cliente.verificar_telefono()
        self.assertFalse(resultado_invalido[0])  # Teléfono inválido

    def test_verificar_email(self):
        cliente = Verificar_Cliente(self.nombre_valido, self.dni_valido, self.direccion_valida, self.telefono_valido, self.email_valido)
        resultado_valido = cliente.verificar_email()
        self.assertTrue(resultado_valido[0])  # Email válido
        
        cliente.email = self.email_invalido
        resultado_invalido = cliente.verificar_email()
        self.assertFalse(resultado_invalido[0])  # Email inválido

    def test_verificar_formulario(self):
        cliente = Verificar_Cliente(self.nombre_valido, self.dni_valido, self.direccion_valida, self.telefono_valido, self.email_valido)
        resultados = cliente.verificar_formulario()
        
        # Verificar que todos los resultados sean válidos
        for campo, (valido, _) in resultados.items():
            self.assertTrue(valido, f"{campo.capitalize()} debe ser válido.")
        
        # Cambiar a valores inválidos y verificar
        cliente.nombre = self.nombre_invalido
        cliente.dni = self.dni_invalido
        cliente.direccion = self.direccion_invalida
        cliente.telefono = self.telefono_invalido
        cliente.email = self.email_invalido
        
        resultados = cliente.verificar_formulario()
        for campo, (valido, _) in resultados.items():
            self.assertFalse(valido, f"{campo.capitalize()} debe ser inválido.")

# Ejecutar los tests
if __name__ == "__main__":
    unittest.main()