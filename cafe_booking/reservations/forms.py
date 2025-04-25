from django import forms
from .models import CustomUser, Cafe, Booking
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']


class CafeForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'address', 'table_count']
        model = Cafe
        fields = ['name', 'motto', 'description', 'address', 'table_count']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['cafe', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
