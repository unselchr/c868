from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)