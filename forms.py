from django.forms import ModelForm
from .models import Mistnost
from django.contrib.auth.models import User
from django import forms

class MistnostForm(ModelForm):
    class Meta:
        model = Mistnost
        fields = '__all__'
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

