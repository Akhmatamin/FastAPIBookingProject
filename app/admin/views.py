from app.database.models import *
from sqladmin import ModelView

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]

class CountryAdmin(ModelView, model=Country):
    column_list = [Country.name]

