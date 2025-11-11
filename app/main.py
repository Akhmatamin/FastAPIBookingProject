from fastapi import FastAPI
import uvicorn
from app.api.endpoints import country, booking,city,hotel,review, room, room_images, hotel_images,service,user,social_auth
from app.admin.setup import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from app.config import SECRET_KEY


hotel_app = FastAPI()

hotel_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

setup_admin(hotel_app)

hotel_app.include_router(social_auth.social_router)
hotel_app.include_router(country.country_router)
hotel_app.include_router(booking.booking_router)
hotel_app.include_router(hotel.hotel_router)
hotel_app.include_router(review.review_router)
hotel_app.include_router(room.room_router)
hotel_app.include_router(room_images.room_image_router)
hotel_app.include_router(hotel_images.hotel_image_router)
hotel_app.include_router(service.service_router)
hotel_app.include_router(user.user_router)
hotel_app.include_router(city.city_router)



if __name__ == '__main__':
    uvicorn.run(hotel_app, host="127.0.0.1", port=8001)
