from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.urls import reverse

class Valute(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    num_code = models.IntegerField()
    char_code = models.CharField(max_length=10)
    nominal = models.IntegerField()
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=20, decimal_places=10)
    previous = models.DecimalField(max_digits=20, decimal_places=10)
class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('city', kwargs={'city_slug': self.slug})
    def get_amount_cars(self):
        count = 0;
        cars = Car.objects.filter(city=self.pk,isSold=False)
        for car in cars:
            count = count + 1
        return count
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    logo = models.ImageField(upload_to='car/brand')

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_slug': self.slug})
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class Car(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    year = models.IntegerField()
    engine_capacity = models.DecimalField(max_digits=4, decimal_places=2)
    run = models.BigIntegerField()
    color = models.CharField(max_length=255)
    description = models.TextField()
    time_created = models.DateField(auto_now_add=True)
    time_updated = models.DateField(auto_now=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to='car/main_image/%Y/%m/%d')
    price = models.BigIntegerField()
    isSold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_amount_ratings(self):
        return len(Ratings.objects.filter(car=self))
   
    def get_absolute_url(self):
        return reverse('car', kwargs={'car_slug': self.slug})
   
    def get_average_rating(self):
        ratings = Ratings.objects.filter(car=self)
        if len(ratings) == 0:
            return 0
        sum = 0
        for rating in ratings:
            sum += rating.rating
        return round(sum / len(ratings), 2)
    
    def get_comments(self):
        comments = Comments.objects.filter(car=self)
        return len(comments)

    def get_count_rating(self):
        ratings = Ratings.objects.filter(car=self)
        return len(ratings)

    def get_visiters(self):
        visits = Visits.objects.filter(car=self)
        return len(visits)

    def get_carts(self):
        carts = Cart.objects.filter(car=self)
        return len(carts)
    
    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def get_absolute_update_url(self):
        return reverse('update-car', kwargs={'car_slug': self.slug})
    def get_absolute_add_url(self):
        return reverse('add-photos-car', kwargs={'car_slug': self.slug})

class Car_photos(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car/images/%Y/%m/%d')

class Comments(models.Model):
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class Visits(models.Model):
    date = models.DateField(auto_now_add=True)
    visiter = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Visit'
        verbose_name_plural = 'Visits'

class Ratings(models.Model):
    date = models.DateField(auto_now_add=True)
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0,
            validators=[
                MaxValueValidator(5),
                MinValueValidator(0)
            ])
    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

class Cart(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

class Purchase(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
