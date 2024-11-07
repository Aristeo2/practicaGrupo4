from DatosMascota import *
import pytest

# test_datos_mascota.py

from DatosMascota import VerificarMascota
import pytest

def test_nombre():
    assert VerificarMascota.nombre("Pepito") == True
    assert VerificarMascota.nombre("") == False
    assert VerificarMascota.nombre("Juan Carlos") == True
    assert VerificarMascota.nombre("R1") == False
    assert VerificarMascota.nombre("Sopa_?") == False
    assert VerificarMascota.nombre("caiman") == False

def test_tipo():
    assert VerificarMascota.tipo("Perro") == True  
    assert VerificarMascota.tipo("Gato") == True    
    assert VerificarMascota.tipo("Pájaro") == False    
    assert VerificarMascota.tipo("") == False

def test_raza():
    assert VerificarMascota.raza("Labrador") == True  
    assert VerificarMascota.raza("") == False                
    assert VerificarMascota.raza("Perrito123") == False      
    assert VerificarMascota.raza("Bulldog@") == False        
    assert VerificarMascota.raza("Raza muy larga que supera los veinte caracteres") == False  
    assert VerificarMascota.raza("Cocker Spaniel") == True  
    assert VerificarMascota.raza("perro") == False

def test_fecha_nacimiento():
    assert VerificarMascota.fecha_nacimiento("01/01/2020") == True
    assert VerificarMascota.fecha_nacimiento("31/12/1999") == True
    assert VerificarMascota.fecha_nacimiento("31/02/2020") == False
    assert VerificarMascota.fecha_nacimiento("01/01/20") == False

def test_patologias():
    assert VerificarMascota.patologias("Alergia") == True  
    assert VerificarMascota.patologias("") == False              
    assert VerificarMascota.patologias("Alergia123") == False    
    assert VerificarMascota.patologias("Fiebre@") == False       
    assert VerificarMascota.patologias("tuberculosis") == False   

def test_dueño():
    assert VerificarMascota.dueño("Juan Perez") == True
    assert VerificarMascota.dueño("") == False
    assert VerificarMascota.dueño("Maria123") == False
    assert VerificarMascota.dueño("Maria@") == False
    assert VerificarMascota.dueño("maria") == False

