from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Enum, DateTime, Text
from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum


class RoleChoices(str, PyEnum):
    client = "client"
    owner = "owner"

class Stars(int, PyEnum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class Country(Base):
    __tablename__ = "country"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(32), unique=True)
    image: Mapped[Optional[str]] = mapped_column(String,nullable=True)

    user_country : Mapped[List['UserProfile']] = relationship('UserProfile',back_populates='country')
    country_hotel : Mapped[List['Hotel']] = relationship('Hotel',back_populates='hotel_country',
                                                        cascade="all, delete-orphan")

    def __repr__(self):
        return f'{self.name}'

class UserProfile(Base):
    __tablename__ = "user_profile"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username : Mapped[str] = mapped_column(String(32), unique=True)
    first_name : Mapped[str] = mapped_column(String(32), nullable=True)
    last_name : Mapped[str] = mapped_column(String(32), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String,nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String,nullable=True, unique=True)
    email : Mapped[Optional[str]] = mapped_column(String,nullable=True, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    created_date : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    country : Mapped[Country] = relationship(Country, back_populates="user_country")

    user_hotels: Mapped[List['Hotel']] = relationship('Hotel',back_populates='owner')

    user_bookings: Mapped[List['Booking']] = relationship('Booking',back_populates='client',
                                                          cascade="all, delete-orphan")
    user_reviews: Mapped[List['Review']] = relationship('Review',back_populates='review_user',
                                                        cascade="all, delete-orphan")
    user_token: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='token_user',
                                                             cascade="all, delete-orphan")

    def __repr__(self):
        return f'{self.first_name, self.last_name}'


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token : Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    token_user:Mapped[UserProfile] = relationship("UserProfile", back_populates="user_token")
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class City(Base):
    __tablename__ = "city"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(32), unique=True)
    image: Mapped[Optional[str]] = mapped_column(String,nullable=True)

    city_hotel: Mapped[List['Hotel']] = relationship('Hotel',back_populates='city',
                                                     cascade="all, delete-orphan")

class Service(Base):
    __tablename__ = "service"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(32), unique=True)
    image : Mapped[str] = mapped_column(String,nullable=True)

class Hotel(Base):
    __tablename__ = "hotel"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String(32))
    hotel_stars: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String,nullable=True)
    postal_code: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped[City] = relationship(City, back_populates="city_hotel")
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    hotel_country: Mapped[Country] = relationship(Country, back_populates="country_hotel")
    owner_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    owner: Mapped[UserProfile] = relationship(UserProfile, back_populates="user_hotels")
    hotel_images: Mapped[List['HotelImage']] = relationship('HotelImage',back_populates='hotel_img',
                                                            cascade="all, delete-orphan")
    hotel_rooms:Mapped[List['Room']] = relationship('Room',back_populates='room_hotel',
                                                    cascade='all, delete-orphan')
    hotel_bookings: Mapped[List['Booking']] = relationship('Booking',back_populates='booking_hotel',
                                                           cascade="all, delete-orphan")
    hotel_reviews: Mapped[List['Review']] = relationship('Review',back_populates='review_hotel',
                                                         cascade="all, delete-orphan")


class HotelImage(Base):
    __tablename__ = "hotel_image"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    images: Mapped[Optional[str]] = mapped_column(String,nullable=True)

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    hotel_img : Mapped[Hotel] = relationship(Hotel, back_populates="hotel_images")

class RoomStatus(str, PyEnum):
    free = "free"
    booked = "booked"
    occupied = "occupied"

class RoomTypes(str, PyEnum):
    lux = "lux"
    half_lux = "half-lux"
    one_suit = "one-suit"
    two_suit = "two-suit"


class Room(Base):
    __tablename__ = "room"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_number: Mapped[int] = mapped_column(Integer)
    price: Mapped[str] = mapped_column(String,nullable=True)
    status: Mapped[RoomStatus] = mapped_column(Enum(RoomStatus), default=RoomStatus.free)
    type: Mapped[RoomTypes] = mapped_column(Enum(RoomTypes), default=RoomTypes.one_suit)

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    room_hotel: Mapped[Hotel] = relationship(Hotel, back_populates="hotel_rooms")
    room_images : Mapped[List['RoomImage']] = relationship('RoomImage',back_populates='room',
                                                           cascade="all, delete-orphan")
    room_bookings: Mapped[List['Booking']] = relationship('Booking',back_populates='booking_room',
                                                          cascade="all, delete-orphan")


class RoomImage(Base):
    __tablename__ = "room_image"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    images: Mapped[Optional[str]] = mapped_column(String,nullable=True)

    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    room : Mapped[Room] = relationship(Room, back_populates="room_images")


class Booking(Base):
    __tablename__ = "booking"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    check_in: Mapped[datetime] = mapped_column(DateTime)
    check_out: Mapped[datetime] = mapped_column(DateTime)
    ordered_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    client_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    client: Mapped[UserProfile] = relationship(UserProfile, back_populates="user_bookings")
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    booking_hotel:Mapped[Hotel] = relationship(Hotel, back_populates="hotel_bookings")
    room_id:Mapped[int] = mapped_column(ForeignKey("room.id"))
    booking_room:Mapped[Room] = relationship(Room, back_populates="room_bookings")


class Review(Base):
    __tablename__ = "review"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment: Mapped[str] = mapped_column(Text,nullable=True)
    stars: Mapped[Stars] = mapped_column(Enum(Stars), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    review_user:Mapped[UserProfile] = relationship(UserProfile, back_populates="user_reviews")
    hotel_id:Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    review_hotel:Mapped[Hotel] = relationship(Hotel,back_populates="hotel_reviews")