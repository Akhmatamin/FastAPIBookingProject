from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .models import RoleChoices, Stars, RoomTypes, RoomStatus


class CountrySchema(BaseModel):
    name: str
    image: Optional[str]

    class Config:
        orm_mode = True


class CountryOutSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]

    class Config:
        orm_mode = True


class UserProfileSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    image: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    password: str
    age: Optional[int]
    role: RoleChoices
    country_id: int

    class Config:
        orm_mode = True


class UserProfileOutSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    image: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    password: str
    age: Optional[int]
    role: RoleChoices
    created_date: datetime
    country_id: int

    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class CitySchema(BaseModel):
    name: str
    image: Optional[str]

    class Config:
        orm_mode = True


class CityOutSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]

    class Config:
        orm_mode = True


class ServiceSchema(BaseModel):
    name: str
    image: str

    class Config:
        orm_mode = True


class ServiceOutSchema(BaseModel):
    id: int
    name: str
    image: str

    class Config:
        orm_mode = True


class HotelSchema(BaseModel):
    hotel_name: str
    hotel_stars: int
    address: str
    postal_code: Optional[int]
    description: str
    city_id : int
    country_id: int
    owner_id: int

    class Config:
        orm_mode = True


class HotelOutSchema(BaseModel):
    id: int
    hotel_name: str
    hotel_stars: int
    address: str
    postal_code: Optional[int]
    description: str
    city_id : int
    country_id: int
    owner_id: int

    class Config:
        orm_mode = True


class HotelImageSchema(BaseModel):
    id: int
    images: Optional[str]
    hotel_id: int

    class Config:
        orm_mode = True


class HotelImageOutSchema(BaseModel):
    id: int
    images: Optional[str]
    hotel_id: int

    class Config:
        orm_mode = True


class RoomSchema(BaseModel):
    room_number: str
    price: int
    status: RoomStatus
    type: RoomTypes
    hotel_id: int

    class Config:
        orm_mode = True


class RoomOutSchema(BaseModel):
    id: int
    room_number: str
    price: int
    status: RoomStatus
    type: RoomTypes
    hotel_id: int

    class Config:
        orm_mode = True


class RoomImageSchema(BaseModel):
    images: Optional[str]
    room_id: int

    class Config:
        orm_mode = True


class RoomImageOutSchema(BaseModel):
    id: int
    images: Optional[str]
    room_id: int

    class Config:
        orm_mode = True


class BookingSchema(BaseModel):
    check_in: datetime
    check_out: datetime
    ordered_date: datetime
    client_id: int
    hotel_id: int
    room_id: int

    class Config:
        orm_mode = True


class BookingOutSchema(BaseModel):
    id: int
    check_in: datetime
    check_out: datetime
    ordered_date: datetime
    client_id: int
    hotel_id: int
    room_id: int

    class Config:
        orm_mode = True


class ReviewSchema(BaseModel):
    comment: str
    stars: Stars
    created_at: datetime
    user_id:int
    hotel_id: int

    class Config:
        orm_mode = True


class ReviewOutSchema(BaseModel):
    id: int
    comment: str
    stars: Stars
    created_at: datetime
    user_id:int
    hotel_id: int

    class Config:
        orm_mode = True
