from fastapi import APIRouter, Depends, HTTPException
from app.database.models import Booking
from app.database.schema import BookingSchema,BookingOutSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

booking_router = APIRouter(prefix="/booking", tags=["Booking"])

@booking_router.post("/create", response_model=BookingOutSchema)
async def create_booking(booking_data: BookingSchema, db: Session = Depends(get_db)):
    booking_db = Booking(**booking_data.dict())
    db.add(booking_db)
    db.commit()
    db.refresh(booking_db)
    return booking_db

@booking_router.get("/all", response_model=List[BookingOutSchema])
async def get_bookings(db: Session = Depends(get_db)):
    booking_db = db.query(Booking).all()
    return booking_db

@booking_router.get("/{booking_id}", response_model=BookingOutSchema)
async def get_booking(booking_id: int, db:Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_db is None:
        return HTTPException(status_code=404, detail="Booking not found")
    return booking_db

@booking_router.put("/{booking_id}", response_model=BookingOutSchema)
async def update_booking(booking_id: int, booking_data:BookingSchema, db:Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_db is None:
        return HTTPException(status_code=404, detail="Booking not found")
    for key, value in booking_data.dict().items():
        setattr(booking_db, key, value)
    db.commit()
    db.refresh(booking_db)
    return booking_db

@booking_router.delete("/{booking_id}")
async def delete_booking(booking_id: int, db:Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_db is None:
        return HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking_db)
    db.commit()
    return {"message": "Booking deleted"}