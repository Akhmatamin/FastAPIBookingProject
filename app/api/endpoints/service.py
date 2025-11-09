from fastapi import APIRouter, Depends, HTTPException
from app.database.models import Service
from app.database.schema import ServiceSchema,ServiceOutSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

service_router = APIRouter(prefix="/service", tags=["Service"])

@service_router.post('/create', response_model=ServiceOutSchema)
async def create_service(service_data : ServiceSchema, db: Session = Depends(get_db)):
    service_db = Service(**service_data.dict())
    db.add(service_db)
    db.commit()
    db.refresh(service_db)
    return service_db

@service_router.get('/all', response_model=List[ServiceOutSchema])
async def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()

@service_router.get('/{service_id}', response_model=ServiceOutSchema)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if service_db is None:
        return HTTPException(status_code=404, detail="Service not found")
    return service_db

@service_router.put('/{service_id}', response_model=ServiceOutSchema)
async def update_service(service_id: int, service_data:ServiceSchema, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if service_db is None:
        return HTTPException(status_code=404, detail="Service not found")
    for key, value in service_data.dict().items():
        setattr(service_db, key, value)
    db.commit()
    db.refresh(service_db)
    return service_db

@service_router.delete('/{service_id}')
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if service_db is None:
        return HTTPException(status_code=404, detail="Service not found")
    db.delete(service_db)
    db.commit()
    return {"message": "Service deleted"}
