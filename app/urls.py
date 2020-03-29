from django.urls import path, include
from app.views import *

urlpatterns = [

    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('register', register, name="register"),
    path('check_code', check_code, name="check_code"),
    path('forget_password', forget_password, name="forget_password"),
    path('change_password', change_password, name="change_password"),
    path('change_name', change_name, name="change_name"),
    path('change_image', change_image, name="change_image"),
    path('index', index, name="index"),
]