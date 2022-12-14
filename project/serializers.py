from rest_framework import serializers
from .models import *
from django.utils.translation import gettext_lazy as _
import re


class CitySerializer(serializers.ModelSerializer):
    persons = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(),
        many=True
    )

    class Meta:
        model = City
        fields = [
            'name',
            'persons'
        ]


class PersonSerializer(serializers.ModelSerializer):
    city_list = CitySerializer(
        many=True,
        read_only=True
    )

    def validate(self, value):
        if not re.fullmatch(REGEX, value['first_name']):
            raise ValidationError(
                _('It must consist of letters only.'),
                params={'value': value},
            )
        if not value['first_name'].istitle():
            raise ValidationError(
                _('First letter can only be capitalized'),
                params={'value': value},
            )
        if not re.fullmatch(REGEX, value['last_name']):
            raise ValidationError(
                _('It must consist of letters only.'),
                params={'value': value},
            )
        if not value['last_name'].istitle():
            raise ValidationError(
                _('First letter can only be capitalized'),
                params={'value': value},
            )
        if value['age'].isalpha():
            raise serializers.ValidationError(
                "The age must consist of only numbers.",
            )
        if not value['default_city'].istitle():
            raise ValidationError(
                _('First letter can only be capitalized'),
                params={'value': value},
            )
        if not re.fullmatch(REGEX, value['default_city']):
            raise ValidationError(
                _('It must consist of letters only.'),
                params={'value': value},
            )

        return value

    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'age',
            'default_city',
            'theme',
            'owner',
            'city_list'
        ]
