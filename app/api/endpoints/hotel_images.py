from fastapi import APIRouter, Depends, HTTPException
from app.database.models import HotelImage
from app.database.schema import HotelImageSchema,HotelImageOutSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

hotel_image_router = APIRouter(prefix="/hotel_image", tags=["HotelImage"])

@hotel_image_router.post('/create', response_model=HotelImageOutSchema)
async def create_hotel_image(hotel_image_data : HotelImageSchema, db: Session = Depends(get_db)):
    hotel_image_db = HotelImage(**hotel_image_data.dict())
    db.add(hotel_image_db)
    db.commit()
    db.refresh(hotel_image_db)
    return hotel_image_db

@hotel_image_router.get('/all', response_model=List[HotelImageOutSchema])
async def get_hotel_images(db: Session = Depends(get_db)):
    return db.query(HotelImage).all()

@hotel_image_router.get('/{hotel_image_id}', response_model=HotelImageOutSchema)
async def get_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if hotel_image_db is None:
        return HTTPException(status_code=404, detail="HotelImage not found")
    return hotel_image_db

@hotel_image_router.put('/{hotel_image_id}', response_model=HotelImageOutSchema)
async def update_hotel_image(hotel_image_id: int, hotel_image_data:HotelImageSchema, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if hotel_image_db is None:
        return HTTPException(status_code=404, detail="HotelImage not found")
    for key, value in hotel_image_data.dict().items():
        setattr(hotel_image_db, key, value)
    db.commit()
    db.refresh(hotel_image_db)
    return hotel_image_db

@hotel_image_router.delete('/{hotel_image_id}')
async def delete_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if hotel_image_db is None:
        return HTTPException(status_code=404, detail="HotelImage not found")
    db.delete(hotel_image_db)
    db.commit()
    return {"message": "HotelImage deleted"}
