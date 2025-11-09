from fastapi import APIRouter, Depends, HTTPException
from app.database.models import Room
from app.database.schema import RoomSchema,RoomOutSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

room_router = APIRouter(prefix="/room", tags=["Room"])

@room_router.post("/create", response_model=RoomOutSchema)
async def create_room(room_data: RoomSchema, db: Session = Depends(get_db)):
    room_db = Room(**room_data.dict())
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return room_db

@room_router.get("/all", response_model=List[RoomOutSchema])
async def get_rooms(db: Session = Depends(get_db)):
    room_db = db.query(Room).all()
    return room_db

@room_router.get("/{room_id}", response_model=RoomOutSchema)
async def get_room(room_id: int, db:Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if room_db is None:
        return HTTPException(status_code=404, detail="Room not found")
    return room_db

@room_router.put("/{room_id}", response_model=RoomOutSchema)
async def update_room(room_id: int, room_data:RoomSchema, db:Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if room_db is None:
        return HTTPException(status_code=404, detail="Room not found")
    for key, value in room_data.dict().items():
        setattr(room_db, key, value)
    db.commit()
    db.refresh(room_db)
    return room_db

@room_router.delete("/{room_id}")
async def delete_room(room_id: int, db:Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if room_db is None:
        return HTTPException(status_code=404, detail="Room not found")
    db.delete(room_db)
    db.commit()
    return {"message": "Room deleted"}