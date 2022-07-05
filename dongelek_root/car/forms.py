from dataclasses import field, fields
from pyexpat import model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from .models import *

# Register form
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['email','username','first_name','last_name','password1','password2']

    def __init__(self, *args, **kwargs):
        
        super(RegisterForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['email'].widget.attrs['class']='form-control'
        self.fields['first_name'].widget.attrs['class']='form-control'
        self.fields['last_name'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'


#
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("name", "slug", "year", "engine_capacity", "run", "color", "city", "brand", "main_image", "price", "description")
class PhotosForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

# AddCar
class AddCar(forms.Form):
    name = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    year = forms.IntegerField()
    engine_capacity = forms.DecimalField(max_digits=4, decimal_places=2)
    run = forms.IntegerField()
    color = forms.CharField(max_length=255)
    city = forms.ModelChoiceField(queryset=City.objects.all())
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    main_image = forms.ImageField()
    price = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}))

    

class AddComment(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}))

class SendEmail(forms.Form):
    Email = forms.EmailField()
    def __str__(self):
        return self.Email
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
