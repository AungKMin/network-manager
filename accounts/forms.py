from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

"""
Form for creating/updating contact
"""
class ContactForm(ModelForm):
    class Meta: 
        model = Contact
        fields = '__all__' 
        exclude = ['user_wrapper']
        
"""
Form for creating/updating contact point
"""
class ContactPointForm(ModelForm):
    class Meta: 
        model = ContactPoint
        fields = '__all__' 

"""
Form for user registration
"""
class CreateUserForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # password2 is for password confirmation 

"""
Form for creating contact tags
"""
class ContactPointMethodForm(ModelForm):
    class Meta: 
        model = ContactPointMethod
        fields = '__all__'

"""
Form for creating contact point methods
"""
class ContactTagForm(ModelForm):
    class Meta: 
        model = ContactTag
        fields = '__all__'
