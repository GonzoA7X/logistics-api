from sqlmodel import create_engine, Session

# Configuración de la base de datos PostgreSQL
# Nota: En un entorno de producción, las credenciales deben provenir de variables de entorno
DATABASE_URL = "postgresql://postgres:password@localhost:5454/logistics"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
