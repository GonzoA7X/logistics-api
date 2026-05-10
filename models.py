from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum

class EstadoPaquete(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_TRANSITO = "EN_TRANSITO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

# --- USUARIOS ---

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

class UsuarioCreate(SQLModel):
    username: str
    password: str

class UsuarioRead(SQLModel):
    id: int
    username: str

# --- HISTORIAL MOVIMIENTOS ---

class MovimientoBase(SQLModel):
    estado: EstadoPaquete
    ubicacion: str = Field(description="Lugar donde se registró el movimiento")
    fecha: datetime = Field(default_factory=datetime.utcnow)
    paquete_id: int = Field(foreign_key="paquete.id")

class Movimiento(MovimientoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paquete: Optional["Paquete"] = Relationship(back_populates="movimientos")

class MovimientoRead(MovimientoBase):
    id: int

# --- PAQUETES ---

class PaqueteBase(SQLModel):
    numero_guia: str = Field(index=True, unique=True, description="Número de guía único del paquete")
    estado_envio: EstadoPaquete = Field(default=EstadoPaquete.PENDIENTE, description="Estado actual del envío")
    direccion_destino: str = Field(description="Dirección de entrega del paquete")
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow, description="Fecha de la última actualización")

class Paquete(PaqueteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movimientos: List[Movimiento] = Relationship(back_populates="paquete", cascade_delete=True)

class PaqueteCreate(PaqueteBase):
    ubicacion_inicial: str = Field(default="Bodega Central", description="Ubicación inicial para el primer registro del historial")

class PaqueteRead(PaqueteBase):
    id: int

class PaqueteUpdate(SQLModel):
    estado_envio: Optional[EstadoPaquete] = None
    direccion_destino: Optional[str] = None
    ubicacion_actual: Optional[str] = Field(default=None, description="Ubicación obligatoria si se cambia el estado")
