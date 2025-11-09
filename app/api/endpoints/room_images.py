from fastapi import APIRouter, Depends, HTTPException
from app.database.models import RoomImage
from app.database.schema import RoomImageSchema,RoomImageOutSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

room_image_router = APIRouter(prefix="/room_image", tags=["RoomImage"])

@room_image_router.post("/create", response_model=RoomImageOutSchema)
async def create_room_image(room_image_data: RoomImageSchema, db: Session = Depends(get_db)):
    room_image_db = RoomImage(**room_image_data.dict())
    db.add(room_image_db)
    db.commit()
    db.refresh(room_image_db)
    return room_image_db

@room_image_router.get("/all", response_model=List[RoomImageOutSchema])
async def get_room_images(db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).all()
    return room_image_db

@room_image_router.get("/{room_image_id}", response_model=RoomImageOutSchema)
async def get_room_image(room_image_id: int, db:Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if room_image_db is None:
        return HTTPException(status_code=404, detail="RoomImage not found")
    return room_image_db

@room_image_router.put("/{room_image_id}", response_model=RoomImageOutSchema)
async def update_room_image(room_image_id: int, room_image_data:RoomImageSchema, db:Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if room_image_db is None:
        return HTTPException(status_code=404, detail="RoomImage not found")
    for key, value in room_image_data.dict().items():
        setattr(room_image_db, key, value)
    db.commit()
    db.refresh(room_image_db)
    return room_image_db

@room_image_router.delete("/{room_image_id}")
async def delete_room_image(room_image_id: int, db:Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if room_image_db is None:
        return HTTPException(status_code=404, detail="RoomImage not found")
    db.delete(room_image_db)
    db.commit()
    return {"message": "RoomImage deleted"}