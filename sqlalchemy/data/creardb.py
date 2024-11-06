from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os





# Conectar a la base de datos SQlite (si el achivo no existe, se crea automáticamente)
engine = create_engine(f'sqlite:///orm.db', echo = True)


#Creamos una sesion para conectarnos a la base de datos
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Crear una un modelo de tabla

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    iban = Column(String, unique=True, nullable=False)
    
    #Relación con Mascota (1:N)
    mascotas = relationship('Mascota', back_populates='cliente')
    
    
#Pongo el ForeignKey del cliente usando la funcion relationship
class Mascota(Base):
    __tablename__ = 'mascotas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    raza = Column(String, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    
    #Relación con Cliente
    clientes = relationship('Cliente', back_populates='mascotas')

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)
 
print("Base de datos y tablas creadas.") 
