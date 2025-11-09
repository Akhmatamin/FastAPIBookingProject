from fastapi import APIRouter, Depends, HTTPException
from app.database.models import Hotel
from app.database.schema import HotelSchema,HotelOutSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

hotel_router = APIRouter(prefix="/hotel", tags=["Hotel"])

@hotel_router.post('/create', response_model=HotelOutSchema)
async def create_hotel(hotel_data : HotelSchema, db: Session = Depends(get_db)):
    hotel_db = Hotel(**hotel_data.dict())
    db.add(hotel_db)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db

@hotel_router.get('/all', response_model=List[HotelOutSchema])
async def get_hotels(db: Session = Depends(get_db)):
    return db.query(Hotel).all()

@hotel_router.get('/{hotel_id}', response_model=HotelOutSchema)
async def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if hotel_db is None:
        return HTTPException(status_code=404, detail="Hotel not found")
    return hotel_db

@hotel_router.put('/{hotel_id}', response_model=HotelOutSchema)
async def update_hotel(hotel_id: int, hotel_data:HotelSchema, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if hotel_db is None:
        return HTTPException(status_code=404, detail="Hotel not found")
    for key, value in hotel_data.dict().items():
        setattr(hotel_db, key, value)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db

@hotel_router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if hotel_db is None:
        return HTTPException(status_code=404, detail="Hotel not found")
    db.delete(hotel_db)
    db.commit()
    return {"message": "Hotel deleted"}
