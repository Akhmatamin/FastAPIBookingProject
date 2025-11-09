from fastapi import APIRouter, Depends, HTTPException
from app.database.models import Country
from app.database.schema import CountrySchema,CountryOutSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

country_router = APIRouter(prefix="/country", tags=["Country"])

@country_router.post('/create', response_model=CountryOutSchema)
async def create_country(country_data : CountrySchema, db: Session = Depends(get_db)):
    country_db = Country(**country_data.dict())
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db

@country_router.get('/', response_model=List[CountryOutSchema])
async def get_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()

@country_router.get('/{country_id}', response_model=CountryOutSchema)
async def get_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if country_db is None:
        return HTTPException(status_code=404, detail="Country not found")
    return country_db

@country_router.put('/{country_id}', response_model=CountryOutSchema)
async def update_country(country_id: int, country_data:CountrySchema, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if country_db is None:
        return HTTPException(status_code=404, detail="Country not found")
    for key, value in country_data.dict().items():
        setattr(country_db, key, value)
    db.commit()
    db.refresh(country_db)
    return country_db

@country_router.delete('/{country_id}', response_model=CountryOutSchema)
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if country_db is None:
        return HTTPException(status_code=404, detail="Country not found")
    db.delete(country_db)
    db.commit()
    return {"message": "Country deleted"}
