from DatosMascota import *
import pytest

def test_nombre():
    # Casos válidos
    assert VerificarMascota.nombre("Pepito") == True
    assert VerificarMascota.nombre("Juan Carlos") == True
    assert VerificarMascota.nombre("José María") == True  # Caracteres con acento
    assert VerificarMascota.nombre("Jean-Luc") == True  # Nombre con guion
    
    # Casos inválidos
    assert VerificarMascota.nombre("") == False  # Nombre vacío
    assert VerificarMascota.nombre("R1") == False  # Contiene número
    assert VerificarMascota.nombre("Sopa_?") == False  # Contiene caracteres especiales
    assert VerificarMascota.nombre("caiman") == False  # Empieza con minúscula
    assert VerificarMascota.nombre("Ana María@") == False  # Contiene un carácter especial (@)

def test_tipo():
    # Casos válidos
    assert VerificarMascota.tipo("Perro") == True  
    assert VerificarMascota.tipo("Gato") == True    

    # Casos inválidos
    assert VerificarMascota.tipo("Pájaro") == False  # Tipo no válido
    assert VerificarMascota.tipo("") == False  # Tipo vacío
    assert VerificarMascota.tipo("Perro Gato") == False  # Tipo combinado, no permitido

def test_raza():
    # Casos válidos
    assert VerificarMascota.raza("Labrador") == True  
    assert VerificarMascota.raza("Cocker Spaniel") == True  # Varios nombres de raza

    # Casos inválidos
    assert VerificarMascota.raza("") == False  # Raza vacía
    assert VerificarMascota.raza("Perrito123") == False  # Contiene números
    assert VerificarMascota.raza("Bulldog@") == False  # Contiene caracteres especiales
    assert VerificarMascota.raza("Raza muy larga que supera los veinte caracteres") == False  # Longitud mayor a 20 caracteres
    assert VerificarMascota.raza("perro") == False  # Empieza con minúscula
    assert VerificarMascota.raza("Pitbull*") == False  # Contiene un carácter especial

def test_fecha_nacimiento():
    # Casos válidos
    assert VerificarMascota.fecha_nacimiento("01/01/2020") == True
    assert VerificarMascota.fecha_nacimiento("31/12/1999") == True

    # Casos inválidos
    assert VerificarMascota.fecha_nacimiento("31/02/2020") == False  # Fecha inválida (febrero no tiene 31)
    assert VerificarMascota.fecha_nacimiento("01/01/20") == False  # Año con 2 dígitos
    assert VerificarMascota.fecha_nacimiento("01/01/2025") == False  # Fecha futura
    assert VerificarMascota.fecha_nacimiento("00/00/2020") == False  # Fecha inválida (día y mes no existen)

def test_patologias():
    # Casos válidos
    assert VerificarMascota.patologias("Alergia") == True  
    assert VerificarMascota.patologias("Hipertensión") == True  # Patología con mayúscula al inicio

    # Casos inválidos
    assert VerificarMascota.patologias("") == False  # Patología vacía
    assert VerificarMascota.patologias("Alergia123") == False  # Contiene números
    assert VerificarMascota.patologias("Fiebre@") == False  # Contiene caracteres especiales
    assert VerificarMascota.patologias("tuberculosis") == False  # Empieza con minúscula
    assert VerificarMascota.patologias("Cancer!") == False  # Contiene un carácter especial

def test_dueño():
    # Casos válidos
    assert VerificarMascota.dueño("Juan Perez") == True
    assert VerificarMascota.dueño("José María López") == True  # Nombre con acento
    assert VerificarMascota.dueño("Jean-Luc Dupont") == True  # Nombre con guion

    # Casos inválidos
    assert VerificarMascota.dueño("") == False  # Dueño vacío
    assert VerificarMascota.dueño("Maria123") == False  # Contiene números
    assert VerificarMascota.dueño("Maria@") == False  # Contiene carácter especial (@)
    assert VerificarMascota.dueño("maria") == False  # Empieza con minúscula
