import pytest
from DatosMascota import VerificarMascota

def test_nombre():
    # Casos válidos
    assert VerificarMascota.nombre("Fido") == True
    assert VerificarMascota.nombre("José-Luis") == True
    assert VerificarMascota.nombre("O'Connor") == True

    # Casos inválidos
    assert VerificarMascota.nombre("") == False  # Vacío
    assert VerificarMascota.nombre("123") == False  # Solo números
    assert VerificarMascota.nombre("Fido#") == False  # Caracter especial no permitido
    assert VerificarMascota.nombre("fido") == False  # No empieza con mayúscula

def test_tipo():
    # Casos válidos
    assert VerificarMascota.tipo("Perro") == True
    assert VerificarMascota.tipo("Gato") == True

    # Casos inválidos
    assert VerificarMascota.tipo("Pájaro") == False
    assert VerificarMascota.tipo("") == False

def test_raza():
    # Casos válidos
    assert VerificarMascota.raza("Labrador") == True
    assert VerificarMascota.raza("Cocker Spaniel") == True
    assert VerificarMascota.raza("Dálmata") == True

    # Casos inválidos
    assert VerificarMascota.raza("") == False  # Vacío
    assert VerificarMascota.raza("12345") == False  # Solo números
    assert VerificarMascota.raza("Bulldog#") == False  # Caracter especial no permitido
    assert VerificarMascota.raza("labrador") == False  # No empieza con mayúscula
    assert VerificarMascota.raza("UnaRazaMuyLargaDeVeinteCaracteres") == False  # Más de 20 caracteres

def test_fecha_nacimiento():
    # Casos válidos
    assert VerificarMascota.fecha_nacimiento("01/01/2020") == True
    assert VerificarMascota.fecha_nacimiento("15/08/2015") == True

    # Casos inválidos
    assert VerificarMascota.fecha_nacimiento("31/02/2020") == False  # Fecha imposible
    assert VerificarMascota.fecha_nacimiento("01/01/2030") == False  # Fecha futura
    assert VerificarMascota.fecha_nacimiento("01-01-2020") == False  # Formato incorrecto

def test_patologias():
    # Casos válidos
    assert VerificarMascota.patologias("Alergia") == True
    assert VerificarMascota.patologias("Problemas Renales") == True
    assert VerificarMascota.patologias("Cólico") == True
    assert VerificarMascota.patologias("COVID-19") == True  # Patología con número
    assert VerificarMascota.patologias("H1N1") == True  # Solo números y letras

    # Casos inválidos
    assert VerificarMascota.patologias("") == False  # Vacío
    assert VerificarMascota.patologias("12345") == False  # Solo números
    assert VerificarMascota.patologias("Infección@") == False  # Caracter especial no permitido
    assert VerificarMascota.patologias("alergia") == False  # No empieza con mayúscula

def test_dueño():
    # Casos válidos
    assert VerificarMascota.dueño("Juan Pérez") == True
    assert VerificarMascota.dueño("María-Luisa") == True

    # Casos inválidos
    assert VerificarMascota.dueño("") == False
    assert VerificarMascota.dueño("12345") == False
    assert VerificarMascota.dueño("Ana@") == False
    assert VerificarMascota.dueño("ana") == False

