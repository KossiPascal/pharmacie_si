from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User
from django.forms import Textarea



class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",'style': "background:white; color:black"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",'style': "background:white; color:black"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",'style': "background:white; color:black"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': "form-control",'style': "background:white; color:black"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control",'style': "background:white; color:black"}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control",'style': "background:white; color:black"}))
    
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirm')

class UserProfileInfoForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, label="Select a file")
    class Meta():
        model = UserProfileInfo
        fields = [
            'profile_pic',
            'biography',
        ]

        widgets = {
            'biography': Textarea(attrs={'cols': 25, 'rows': 5, 'class': "form-control", 'style': "background:white; color:black"}),
        }

class ProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "control",'disabled': "disabled",'style': "width:100%; border:none!important; padding:2px 5px; background:none; color:black"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",'style': "background:white; color:black"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",'style': "background:white; color:black"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': "control",'disabled': "disabled",'style': "width:100%; border:none!important; padding:2px 5px; background:none; color:black"}))
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
