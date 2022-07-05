from cProfile import run
from django.contrib import messages
from django.shortcuts import *
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from car.models import *
from .forms import *
from django.core.mail import send_mail
from dongelek.settings import EMAIL_HOST_USER
import os.path
import requests
import json
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


from urllib.request import urlopen
from django.shortcuts import render,redirect


# Create your views here.

menu = [
    {'title': "About site",
     'url_name': 'about'},
]
valutes = Valute.objects.all()


# Index home page
def index(request):
    brands = Brand.objects.all()
    cities = City.objects.all()
    context = {
        'title': "Main Page",
        'menu': menu,
        'brands': brands,
        'cities': cities,
        'valutes': valutes,
    }
    return render(request, 'car/index.html', context)

def update_currency(request):
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = urlopen(url)
    data_json = json.loads(response.read())
    for v_id, v_info in data_json['Valute'].items():
        Valute.objects.filter(id=v_info["ID"]).update(id=v_info["ID"], num_code=v_info["NumCode"],
                              char_code=v_info["CharCode"], nominal=v_info["Nominal"],
                              name=v_info["Name"], value=v_info["Value"], previous=v_info["Previous"])
    return redirect('profile')
# Registration 
def register_request(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('login')
    return render(request, 'car/register.html', {
        'form': form
    })


# Login
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    else:
        return render(request, 'car/login.html')

    # Logout


def logout_request(request):
    logout(request)
    return redirect('home')


# About
def about(request):
    context = {
        'title': "About",
        'menu': menu,
        'valutes': valutes,
    }
    return render(request, 'car/about.html', context)


# Profile
def profile(request):
    cars = Car.objects.filter(seller=request.user)
    context = {
        'title': 'My profile',
        'menu': menu,
        'cars': cars,
        'valutes': valutes,
        'seller':request.user
    }
    return render(request, 'car/profile.html', context)


# add_car
def add_car(request):
    if request.method == 'POST':
        form = AddCar(request.POST, request.FILES)
        if form.is_valid():
            try:
                Car.objects.create(**form.cleaned_data, seller=request.user)
                return redirect('home')
            except:
                form.add_error(None, "There are some errors")
    else:
        form = AddCar()
    context = {
        'title': "Add a new ad",
        'menu': menu,
        'form': form,
        'valutes': valutes,
    }
    return render(request, 'car/addCar.html', context)


def brand(request, brand_slug):
    chosen_brand = Brand.objects.get(slug=brand_slug)
    cars = Car.objects.filter(brand_id=chosen_brand.pk,isSold=False)
    if request.method == 'GET':
        form = request.GET.get('sort')
        if form == 'priceup':
            cars = cars.order_by('price')
        elif form == 'pricedown':
            cars = cars.order_by('-price')
        elif form == 'news':
            cars = cars.order_by('-time_created')
        elif form == 'olds':
            cars = cars.order_by('time_created')
    context = {
        'title': chosen_brand.name,
        'menu': menu,
        'cars': cars,
        'valutes': valutes,
        'brand': chosen_brand,
        
    }

    return render(request, 'car/brand.html', context)


def city(request, city_slug):
    city = City.objects.get(slug=city_slug)
    cars = Car.objects.filter(city_id=city.pk,isSold=False)
    if request.method =='GET':
        form = request.GET.get('sort')
        if form == 'priceup':
            cars = cars.order_by('price')
        elif form == 'pricedown':
            cars = cars.order_by('-price')
        elif form == 'news':
            cars = cars.order_by('-time_created')
        elif form == 'olds':
            cars = cars.order_by('time_created')
    context = {
        'valutes': valutes,
        'title': city.name,
        'menu': menu,
        'cars': cars,
        'brand': city,
    }
    return render(request, 'car/brand.html', context)

def cart(request):
    cars = Cart.objects.filter(user=request.user)
    context = {
        'valutes': valutes,
        'title': 'Your cart',
        'menu': menu,
        'cars': cars,
    }
    return render(request, 'car/cart.html', context)


def car(request, car_slug):
    car = Car.objects.get(slug=car_slug)
    photos = Car_photos.objects.filter(car=car)
    seller = User.objects.get(pk=car.seller.pk)
    if request.user.is_authenticated and car.seller != request.user:
        Visits(car=car, visiter=request.user).save()
    comments = Comments.objects.filter(car=car).order_by('-pk')
    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
            try:
                Comments.objects.create(**form.cleaned_data, author=request.user, car=car)
                request.POST = None
                return redirect(car.get_absolute_url())
            except:
                form.add_error(None, "There are some errors")
        form = AddComment()
    else:
        form = AddComment()
    context = {
        'title': car.name,
        'valutes': valutes,
        'menu': menu,
        'form': form,
        'seller': seller,
        'comments': comments,
        'car': car,
        'photos': photos,
    }
    cart = Cart.objects.filter(car=car.pk, user=request.user.pk)
    if len(cart) > 0:
        context['cart'] = True
    else:
        context['cart'] = False
    if car.get_average_rating() == 0:
        context['rating'] = False
    else:
        context['rating'] = car.get_average_rating()
    return render(request, 'car/car.html', context)


def rate_car(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        car_id = request.POST.get('car')
        car = Car.objects.get(pk=car_id,isSold=False)
        rater = request.user
        Ratings.objects.filter(car=car, rater=rater).delete()
        Ratings.objects.create(rating=rating, car=car, rater=rater).save()
        return JsonResponse({'success': 'true', 'score': rating}, safe=False)
    return JsonResponse({'success:': 'false'})


def add_to_cart(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_basket')
        car = Car.objects.get(pk=car_id,isSold=False)
        user = request.user
        Cart.objects.filter(car=car, user=user).delete()
        Cart.objects.create(car=car, user=user).save()
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success:': 'false'})


def delete_from_cart(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_basket')
        car = Car.objects.get(pk=car_id,isSold=False)
        user = request.user
        Cart.objects.filter(car=car, user=user).delete()
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success:': 'false'})


def delete_car(request):
    if request.method == 'POST':
        car_id = request.POST.get('car')
        car = Car.objects.filter(pk=car_id,isSold=False).delete()
        print(car)
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success:': 'false'})


def send_email(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_interested')
        car = Car.objects.get(pk=car_id,isSold=False)
        seller_email = request.POST.get('seller_email')
        seller_username = request.POST.get('seller_username')
        subject = 'Someone is interested to your car '
        message = request.user.username + " ( " + request.user.email + " )" + " is interested  to your " + str(car)
        send_mail(subject, message,
                  EMAIL_HOST_USER, [seller_email], fail_silently=False)
        subject = "From Dongelek.kz"
        message = "You've interested to " + str(car) + ". Wait answer from " + seller_username
        send_mail(subject, message,
                  EMAIL_HOST_USER, [request.user.email], fail_silently=False)
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success:': 'false'})


def update_car(request, car_slug):
    car = Car.objects.get(slug=car_slug)
    if request.method == 'POST':
        form = AddCar(request.POST, request.FILES)
        if form.is_valid():
            try:
                os.remove(car.main_image.path)
                car.name = form.cleaned_data['name']
                car.slug = form.cleaned_data['slug']
                car.year = form.cleaned_data['year']
                car.engine_capacity = form.cleaned_data['engine_capacity']
                car.run = form.cleaned_data['run']
                car.color = form.cleaned_data['color']
                car.city = form.cleaned_data['city']
                car.brand = form.cleaned_data['brand']
                car.main_image = form.cleaned_data['main_image']
                car.price = form.cleaned_data['price']
                car.description = form.cleaned_data['description']
                car.save()
                return redirect('profile')
            except:
                form.add_error(None, "There are some errors")
    form = CarForm(instance=car)
    context = {
        'valutes': valutes,
        'title': "Updating data about " + car.name,
        'menu': menu,
        'car': car,
        'form': form,
        'car': car,
    }
    if car.seller == request.user:
        return render(request, 'car/update.html', context)
    return render(request, 'car/index.html', context)


def add_photos_car(request, car_slug):
    car = Car.objects.get(slug=car_slug)
    if request.method == 'POST':
        form = PhotosForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        for image in files:
            Car_photos.objects.create(car=car, image=image).save()
        return redirect('profile')
    else:
        form = PhotosForm()
    context = {
        'valutes': valutes,
        'title': "Add new photos",
        'menu': menu,
        'form': form,
        'car': car,
    }
    return render(request, 'car/addPhotos.html', context)


def searchbar(request):
    context = {
        'brands': Brand.objects.all(),
        'cities': City.objects.all(),
        'valutes': valutes,
        'title': "Search Results",
        'menu': menu,
    }
    if request.method == 'GET':
        post = {}
        if request.GET.getlist('city'):
            if request.GET.get('search'):
                search = request.GET.get('search')
                context['search'] = search
                post = Car.objects.filter(name__icontains=search, city__name__in=request.GET.getlist('city'), brand__name__in=request.GET.getlist('brand'), isSold=False)
            else:
                post = Car.objects.filter(city__name__in=request.GET.getlist('city'), brand__name__in=request.GET.getlist('brand'),isSold=False)
        elif request.GET.get('search'):
            search = request.GET.get('search')
            context['search'] = search
            post = Car.objects.filter(name__icontains=search,isSold=False)
        context['post'] = post

        return render(request, 'car/searchbar.html', context)
def purchase(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart')
        cart = Cart.objects.get(pk=cart_id)
        user = cart.user
        car = cart.car
        car.isSold = True
        car.save()
        Purchase.objects.create(user=user, car=car).save()
        cart.delete()
    return redirect('purchases')
def purchases(request):
    context = {
        'cars': Purchase.objects.filter(user=request.user),
        'valutes': valutes,
        'title': "My purchases",
        'menu': menu,
    }
    return render(request, 'car/purchase.html', context)
def purchase_pdf(request):
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase')
        purchase = Purchase.objects.get(pk=purchase_id)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)
        lines = []
        lines.append("Customer:" + str(purchase.user))
        lines.append("Product:" + str(purchase.car))
        lines.append("Seller:" + str(purchase.car.seller))
        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename='purchase.pdf')

def update_user(request):
    context = {
        'valutes': valutes,
        'title': "Update your profile",
        'menu': menu,
    }
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
        else:
            context['error'] = "Enter unique username and email, also check out first name and last name accuracy"
    return render(request, 'car/update_user.html', context)
def my_advertisements(request):
    cars = Car.objects.filter(seller=request.user)
    context = {
        'title': 'My Advertisements',
        'menu': menu,
        'cars': cars,
        'valutes': valutes,
        'seller': request.user
    }
    return render(request, 'car/my_advertisements.html', context)
