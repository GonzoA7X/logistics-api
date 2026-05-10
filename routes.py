from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from database import get_session
from models import Paquete, PaqueteCreate, PaqueteRead, PaqueteUpdate, Movimiento, MovimientoRead, Usuario
from auth import get_current_user

# Añadir dependencias globales para que todas las rutas requieran el token JWT
router = APIRouter(
    prefix="/paquetes", 
    tags=["Paquetes"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=PaqueteRead)
def create_paquete(*, session: Session = Depends(get_session), paquete: PaqueteCreate):
    # Crear el paquete
    db_paquete = Paquete.model_validate(paquete)
    session.add(db_paquete)
    
    try:
        session.commit()
        session.refresh(db_paquete)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Ya existe un paquete con este número de guía")
    
    # Crear el movimiento inicial
    movimiento_inicial = Movimiento(
        estado=db_paquete.estado_envio,
        ubicacion=paquete.ubicacion_inicial,
        paquete_id=db_paquete.id
    )
    session.add(movimiento_inicial)
    session.commit()
    
    return db_paquete

@router.get("/", response_model=List[PaqueteRead])
def read_paquetes(
    *, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)
):
    paquetes = session.exec(select(Paquete).offset(offset).limit(limit)).all()
    return paquetes

@router.get("/{paquete_id}", response_model=PaqueteRead)
def read_paquete(*, session: Session = Depends(get_session), paquete_id: int):
    paquete = session.get(Paquete, paquete_id)
    if not paquete:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    return paquete

@router.patch("/{paquete_id}", response_model=PaqueteRead)
def update_paquete(*, session: Session = Depends(get_session), paquete_id: int, paquete: PaqueteUpdate):
    db_paquete = session.get(Paquete, paquete_id)
    if not db_paquete:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    
    paquete_data = paquete.model_dump(exclude_unset=True)
    
    # Validar que si cambia el estado, debe traer una ubicación
    if "estado_envio" in paquete_data and "ubicacion_actual" not in paquete_data:
        raise HTTPException(status_code=400, detail="Debes proveer 'ubicacion_actual' cuando cambias el estado del paquete")
        
    for key, value in paquete_data.items():
        if key != "ubicacion_actual": # No guardar esto en el paquete directamente
            setattr(db_paquete, key, value)
    
    db_paquete.fecha_actualizacion = datetime.utcnow()
    session.add(db_paquete)
    
    # Si hubo cambio de estado, registramos el movimiento en el historial
    if "estado_envio" in paquete_data:
        nuevo_movimiento = Movimiento(
            estado=db_paquete.estado_envio,
            ubicacion=paquete.ubicacion_actual,
            paquete_id=db_paquete.id
        )
        session.add(nuevo_movimiento)
    
    session.commit()
    session.refresh(db_paquete)
    return db_paquete

@router.delete("/{paquete_id}")
def delete_paquete(*, session: Session = Depends(get_session), paquete_id: int):
    paquete = session.get(Paquete, paquete_id)
    if not paquete:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    session.delete(paquete)
    session.commit()
    return {"ok": True, "message": "Paquete y su historial eliminados exitosamente"}

# --- NUEVO ENDPOINT DE HISTORIAL ---
@router.get("/{paquete_id}/movimientos", response_model=List[MovimientoRead])
def read_paquete_movimientos(*, session: Session = Depends(get_session), paquete_id: int):
    paquete = session.get(Paquete, paquete_id)
    if not paquete:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    
    # Retornar los movimientos ordenados por fecha ascendente
    movimientos = session.exec(
        select(Movimiento).where(Movimiento.paquete_id == paquete_id).order_by(Movimiento.fecha)
    ).all()
    
    return movimientos
