from fastapi import APIRouter, Depends, HTTPException
from app.database.models import City
from app.database.schema import CitySchema,CityOutSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

city_router = APIRouter(prefix="/city", tags=["City"])

@city_router.post('/create', response_model=CityOutSchema)
async def create_city(city_data : CitySchema, db: Session = Depends(get_db)):
    city_db = City(**city_data.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.get('/all', response_model=List[CityOutSchema])
async def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()

@city_router.get('/{city_id}', response_model=CityOutSchema)
async def get_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if city_db is None:
        return HTTPException(status_code=404, detail="City not found")
    return city_db

@city_router.put('/{city_id}', response_model=CityOutSchema)
async def update_city(city_id: int, city_data:CitySchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if city_db is None:
        return HTTPException(status_code=404, detail="City not found")
    for key, value in city_data.dict().items():
        setattr(city_db, key, value)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.delete('/{city_id}')
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if city_db is None:
        return HTTPException(status_code=404, detail="City not found")
    db.delete(city_db)
    db.commit()
    return {"message": "City deleted"}
