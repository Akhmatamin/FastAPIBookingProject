from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from app.config import SECRET_KEY, ALGORITHM
from app.database.models import UserProfile, RefreshToken
from app.database.schema import UserProfileSchema,UserProfileOutSchema, LoginSchema
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List, Optional
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_router = APIRouter(prefix="/user", tags=["UserProfile"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=20))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=10))


@user_router.post("/register", response_model=UserProfileOutSchema)
async def create_user(user_data: UserProfileSchema, db: Session = Depends(get_db)):
    username = db.query(UserProfile).filter(UserProfile.username == user_data.username).first()
    email = db.query(UserProfile).filter(UserProfile.email == user_data.email).first()


    if username:
        raise HTTPException(status_code=400, detail="Username already registered")
    elif email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    user_db = UserProfile(
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        image=user_data.image,
        phone_number=user_data.phone_number,
        email=user_data.email,
        age=user_data.age,
        role=user_data.role,
        country_id=user_data.country_id,
        password=hashed_password
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.post('/login')
async def login(form_data:LoginSchema = Depends() ,db:Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password or username")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    new_token = RefreshToken(user_id=user.id,token=refresh_token)
    db.add(new_token)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token,'token_type': 'bearer'}

@user_router.post("/logout")
async def logout(refresh_token: str, db:Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    db.delete(token_db)
    db.commit()
    return {"message": "Logged out"}

@user_router.get("/all", response_model=List[UserProfileOutSchema])
async def get_users(db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).all()
    return user_db

@user_router.get("/{user_id}", response_model=UserProfileOutSchema)
async def get_user(user_id: int, db:Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        return HTTPException(status_code=404, detail="User not found")
    return user_db

@user_router.put("/{user_id}", response_model=UserProfileOutSchema)
async def update_user(user_id: int, user_data:UserProfileSchema, db:Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        return HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.dict().items():
        setattr(user_db, key, value)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.delete("/{user_id}")
async def delete_user(user_id: int, db:Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        return HTTPException(status_code=404, detail="User not found")
    db.delete(user_db)
    db.commit()
    return {"message": "User deleted"}


@user_router.post('/refresh')
async def refresh(refresh_token: str, db:Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not token_db:
        raise HTTPException(status_code=401, detail="Invalid token")

    access_token = create_access_token({"sub": token_db.id})

    return {'access_token': access_token, 'token_type': 'bearer'}



