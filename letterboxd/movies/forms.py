from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['imageUrl', 'name', 'description', 'age', 'director', 'genre']

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'is_superuser', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_superuser'].widget = forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-green-500'})
        self.fields['is_staff'].widget = forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-green-500'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = self.cleaned_data.get('is_superuser')
        user.is_staff = self.cleaned_data.get('is_staff')
        if commit:
            try:
                user.save()
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
        return user
    

