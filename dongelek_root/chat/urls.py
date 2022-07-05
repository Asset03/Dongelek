from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view

from chat.views import *

urlpatterns = [
    path('', profile, name='profile'),
]