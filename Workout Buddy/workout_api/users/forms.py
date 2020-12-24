#used to manage the form for registering and can add in other input fields

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#inherate UserCreatioForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    #nested name space for configurations for forms and keep them in one place
    class Meta:
        #model that will be affected.
        model = User
        #order in which we want the input fields to be in.
        fields = ['username', 'email', 'password1', 'password2']