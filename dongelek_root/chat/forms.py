from dataclasses import field, fields
from pyexpat import model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms

# Register form

class AddMessage(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':20, 'rows':1}))
