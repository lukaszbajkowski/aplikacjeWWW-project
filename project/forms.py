from django import forms
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = (
            'first_name',
            'last_name',
            'age',
            'default_city',
            'theme'
        )


class EditUserForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = (
            'first_name',
            'last_name',
            'default_city',
            'theme'
        )


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = (
            'name',
            'persons',
        )


class EditCityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = (
            'persons',
        )
