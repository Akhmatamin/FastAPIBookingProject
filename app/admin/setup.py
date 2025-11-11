from .views import UserProfileAdmin, CountryAdmin
from fastapi import FastAPI
from sqladmin import Admin
from app.database.db import engine


def setup_admin(app: FastAPI):
    admin = Admin(app,engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CountryAdmin)

