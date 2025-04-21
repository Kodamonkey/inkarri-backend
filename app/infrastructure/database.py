from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener los valores de las variables de entorno
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Crear la URL de conexión para SQLAlchemy
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseConnection:
    """Clase para manejar la conexión a la base de datos usando SQLAlchemy."""

    def __init__(self):
        self.engine = None
        self.SessionLocal = None

    def connect(self):
        """Establece la conexión a la base de datos."""
        try:
            self.engine = create_engine(DATABASE_URL)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            print("Conexión exitosa a la base de datos con SQLAlchemy")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def get_session(self):
        """Devuelve una nueva sesión de base de datos."""
        if not self.engine:
            self.connect()
        return self.SessionLocal()

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.engine:
            self.engine.dispose()
            print("Conexión cerrada")

# Crear una instancia global de la conexión
connection = DatabaseConnection()
