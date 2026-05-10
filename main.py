from fastapi import FastAPI
from sqlmodel import SQLModel

from database import engine
from routes import router as paquetes_router
from auth_routes import router as auth_router

def create_db_and_tables():
    # Crea todas las tablas definidas en SQLModel (Usuario, Paquete, Movimiento)
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="API de Trazabilidad Logística",
    description="API RESTful para la gestión y trazabilidad de paquetes con autenticación JWT",
    version="2.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluir las rutas de autenticación
app.include_router(auth_router)

# Incluir las rutas de paquetes
app.include_router(paquetes_router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Trazabilidad Logística. Ve a /docs para ver la documentación interactiva."}
