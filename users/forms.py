from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from random import randint


class SignInForm(forms.ModelForm):
    a = randint(20,50)
    b = randint(1,20)
    summation=forms.IntegerField(label=f"{a} + {b} =", required=True, help_text="Proof you are not a robot.")

    class Meta:
        model = User
        fields = ('username', 'password', "summation")
        widgets = {
            'password': forms.PasswordInput(),
        }

    def verification(self):
        s = self.a + self.b
        return s


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["api_key"]
        widgets = {'api_key': forms.PasswordInput(),}