from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home , name='home'),
    path('login', login_attempt , name='login'),
    path('register', register, name='register'),
    path('succes', success, name='succes'),
    path('token', token_send, name='token'),
    path('verify/<auth_token>', verify, name= 'verify'),
    path('error', error_page, name= 'error'),
]
