from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select

from database import engine, get_session
from routes import router as paquetes_router
from auth_routes import router as auth_router
from models import Paquete, Movimiento

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="API de Trazabilidad Logística",
    description="API RESTful para la gestión y trazabilidad de paquetes",
    version="2.0.0"
)

# --- CONFIGURACIÓN DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluir las rutas
app.include_router(auth_router)
app.include_router(paquetes_router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Trazabilidad Logística."}

# --- RUTA PÚBLICA DE RASTREO (SIN JWT) ---
@app.get("/rastreo/{numero_guia}", tags=["Público"])
def rastrear_paquete(*, session: Session = Depends(get_session), numero_guia: str):
    paquete = session.exec(select(Paquete).where(Paquete.numero_guia == numero_guia)).first()
    
    if not paquete:
        raise HTTPException(status_code=404, detail="Número de guía no encontrado")
    
    movimientos = session.exec(
        select(Movimiento).where(Movimiento.paquete_id == paquete.id).order_by(Movimiento.fecha.desc())
    ).all()
    
    return {
        "paquete": paquete,
        "historial": movimientos
    }
