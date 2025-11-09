from fastapi import APIRouter, Depends, HTTPException
from app.database.models import Review
from app.database.schema import ReviewSchema,ReviewOutSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

review_router = APIRouter(prefix="/review", tags=["Review"])

@review_router.post("/create", response_model=ReviewOutSchema)
async def create_review(review_data: ReviewSchema, db: Session = Depends(get_db)):
    review_db = Review(**review_data.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get("/all", response_model=List[ReviewOutSchema])
async def get_reviews(db: Session = Depends(get_db)):
    review_db = db.query(Review).all()
    return review_db

@review_router.get("/{review_id}", response_model=ReviewOutSchema)
async def get_review(review_id: int, db:Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        return HTTPException(status_code=404, detail="Review not found")
    return review_db

@review_router.put("/{review_id}", response_model=ReviewOutSchema)
async def update_review(review_id: int, review_data:ReviewSchema, db:Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        return HTTPException(status_code=404, detail="Review not found")
    for key, value in review_data.dict().items():
        setattr(review_db, key, value)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.delete("/{review_id}")
async def delete_review(review_id: int, db:Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        return HTTPException(status_code=404, detail="Review not found")
    db.delete(review_db)
    db.commit()
    return {"message": "Review deleted"}