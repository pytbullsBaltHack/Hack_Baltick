from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from webface.models import StreamSource


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = ['image']
        fields = []


class SourceAddForm(forms.ModelForm):
    class Meta:
        model = StreamSource
        fields = ['camera_source', 'event_id']
        widgets = {
            'camera_source': forms.TextInput(attrs={'placeholder': 'Camera Source'}),
            'event_id': forms.TextInput(attrs={'placeholder': 'Event Id'})
        }
