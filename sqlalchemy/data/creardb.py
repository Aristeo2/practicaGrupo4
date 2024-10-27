from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


#Especifica la ruta de la base de datos
db_path = os.path.join("/clinica-veterinaria/sqlalchemy", "data-base.db")

# Conectar a la base de datos SQlite (si el achivo no existe, se crea automáticamente)
engine = create_engine(f'sqlite:///{db_path}', echo = True)
Base = declarative_base()

# rear una un modelo de tabla

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    iban = Column(String, unique=True, nullable=False)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)
 
print("Base de datos y tablas creadas.") 