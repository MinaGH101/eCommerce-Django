from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import *


class RegisterForm(forms.Form):
    # first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    # last_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email'}))
    phone = forms.CharField(max_length=17, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Example: 09123456789'}))
    passwordd = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter your password'}))
    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email is already registered !!')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username is already taken !!')
        return username
    
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter username',}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'enter email',}))
    
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name','phone', 'address1', 'address2', 'area', 'state', 'postal_code', 'image')

        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter your first name',}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter your last name',}),
            'phone' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter phone number',}),
            'address1' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
            'address2' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
            'area' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
            'state' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
            'postal_code' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'',}),
            'image': forms.FileInput()
        }
