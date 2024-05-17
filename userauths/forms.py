from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name','class':'with-border'}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username','class':'with-border'}))
    email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email','class':'with-border'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone','class':'with-border'}))
    GENDER_CHOICES = (
         ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gender','class':'with-border'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password','class':'with-border'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password','class':'with-border'}))

    class Meta:
        model = get_user_model()
        fields = ['full_name', 'username', 'email', 'phone', 'gender', 'password1', 'password2']
