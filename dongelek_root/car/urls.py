from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view

from car.views import *



urlpatterns = [
    path('', index, name='home'),
    path('register/', register_request, name='register'),
    path('login/', login_request, name='login'),
    path('logout/',logout_request,name ='logout'),
    path('about/', about, name='about'),
    path('profile/', profile, name='profile'),
    path('add_car/', add_car, name='add_car'),
    path('brand/<slug:brand_slug>/', brand, name='brand'),
    path('car/<slug:car_slug>/', car, name='car'),
    path('city/<slug:city_slug>/', city, name='city'),
    path('rate-car/', rate_car, name='rate-car'),
    path('logout/',logout_request,name ='logout'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('your-cart', cart, name='your-cart'),
    path('send-email/', send_email, name='send-email'),
    path('delete-from-cart/', delete_from_cart, name='delete-from-cart'),
    path('delete-car/', delete_car, name='delete-car'),
    path('update-car/<slug:car_slug>/', update_car, name='update-car'),
    path('add-photos-car/<slug:car_slug>/', add_photos_car, name='add-photos-car'),
    path('searchbar/', searchbar, name='searchbar'),
    path('update-currency/', update_currency, name='update-currency'),
    path('purchase_pdf', purchase_pdf, name='purchase_pdf'),
    path('purchase/', purchase, name='purchase'),
    path('purchases/', purchases, name='purchases'),
    path('update-user/', update_user, name='update-user'),
    path('my-advertisements/', my_advertisements, name='my-advertisements'),

]