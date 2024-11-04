import unittest
from datoscliente import Verificar_Cliente 

class TestVerificar_Cliente(unittest.TestCase):

    def test_verificar_nombre(self):
        # Casos válidos
        self.assertEqual(Verificar_Cliente.verificar_nombre("Juan Pérez"), (True, "Nombre válido."))
        self.assertEqual(Verificar_Cliente.verificar_nombre("Ana"), (True, "Nombre válido."))
        
        # Casos inválidos
        self.assertEqual(Verificar_Cliente.verificar_nombre(""), (False, "El nombre debe tener entre 2 y 50 caracteres."))
        self.assertEqual(Verificar_Cliente.verificar_nombre("J"), (False, "El nombre debe tener entre 2 y 50 caracteres."))
        self.assertEqual(Verificar_Cliente.verificar_nombre("J"*51), (False, "El nombre debe tener entre 2 y 50 caracteres."))
        self.assertEqual(Verificar_Cliente.verificar_nombre("Juan123"), (False, "El nombre solo puede contener letras y espacios."))

    def test_verificar_dni(self):
        # Casos válidos
        self.assertEqual(Verificar_Cliente.verificar_dni("12345678R"), (True, "DNI válido."))
        self.assertEqual(Verificar_Cliente.verificar_dni("87654321"), (True, "DNI válido."))
        
        # Casos inválidos
        self.assertEqual(Verificar_Cliente.verificar_dni("1234567"), (False, "Formato de DNI no válido."))
        self.assertEqual(Verificar_Cliente.verificar_dni("12345678RR"), (False, "Formato de DNI no válido."))
        self.assertEqual(Verificar_Cliente.verificar_dni("abcdefgh"), (False, "Formato de DNI no válido."))

    def test_verificar_direccion(self):
        # Casos válidos
        self.assertEqual(Verificar_Cliente.verificar_direccion("Calle Falsa 123"), (True, "Dirección válida."))
        self.assertEqual(Verificar_Cliente.verificar_direccion("Av. Siempreviva 742"), (True, "Dirección válida."))

        # Casos inválidos
        self.assertEqual(Verificar_Cliente.verificar_direccion(""), (False, "La dirección debe tener entre 5 y 100 caracteres."))
        self.assertEqual(Verificar_Cliente.verificar_direccion("1234"), (False, "La dirección debe tener entre 5 y 100 caracteres."))
        self.assertEqual(Verificar_Cliente.verificar_direccion("C"*101), (False, "La dirección debe tener entre 5 y 100 caracteres."))

    def test_verificar_telefono(self):
        # Casos válidos
        self.assertEqual(Verificar_Cliente.verificar_telefono("123456789"), (True, "Teléfono válido."))
        self.assertEqual(Verificar_Cliente.verificar_telefono("9876543210"), (True, "Teléfono válido."))
        
        # Casos inválidos
        self.assertEqual(Verificar_Cliente.verificar_telefono("12345"), (False, "El teléfono debe contener solo dígitos y tener entre 7 y 15 caracteres."))
        self.assertEqual(Verificar_Cliente.verificar_telefono("1234567890123456"), (False, "El teléfono debe contener solo dígitos y tener entre 7 y 15 caracteres."))
        self.assertEqual(Verificar_Cliente.verificar_telefono("telefono"), (False, "El teléfono debe contener solo dígitos y tener entre 7 y 15 caracteres."))

    def test_verificar_email(self):
        # Casos válidos
        self.assertEqual(Verificar_Cliente.verificar_email("juan.perez@example.com"), (True, "Correo electrónico válido."))
        self.assertEqual(Verificar_Cliente.verificar_email("test123@domain.co"), (True, "Correo electrónico válido."))
        
        # Casos inválidos
        self.assertEqual(Verificar_Cliente.verificar_email("juan.perez"), (False, "Formato de correo electrónico no válido."))
        self.assertEqual(Verificar_Cliente.verificar_email("juan@perez@domain.com"), (False, "Formato de correo electrónico no válido."))
        self.assertEqual(Verificar_Cliente.verificar_email("juan.perez@domain"), (False, "Formato de correo electrónico no válido."))

    def test_verificar_formulario(self):
        # Caso válido
        resultados = Verificar_Cliente.verificar_formulario(
            "Juan Pérez",
            "12345678R",
            "Calle Falsa 123, Ciudad",
            "123456789",
            "juan.perez@example.com"
        )
        for campo, (valido, mensaje) in resultados.items():
            self.assertTrue(valido, f"{campo.capitalize()} debe ser válido. Mensaje: {mensaje}")

        # Caso inválido: varios campos incorrectos
        resultados = Verificar_Cliente.verificar_formulario(
            "Juan123",            # Nombre inválido
            "1234567",            # DNI inválido
            "C",                  # Dirección inválida
            "12345",              # Teléfono inválido
            "juan.perez@domain"   # Email inválido
        )
        for campo, (valido, mensaje) in resultados.items():
            self.assertFalse(valido, f"{campo.capitalize()} debe ser inválido. Mensaje: {mensaje}")

if __name__ == "__main__":
    unittest.main()