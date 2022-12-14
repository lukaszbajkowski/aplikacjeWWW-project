from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework import serializers, request
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

THEME = (
    ('Light', 'Light'),
    ('Dark', 'Dark'),
    ('Default', 'Default'),
)

REGEX = "^[a-zA-Z][a-zA-Z .,'-]*$"


def LettersOnlyValidator(value):
    if not re.fullmatch(REGEX, value):
        raise ValidationError(
            _('It must consist of letters only.'),
            params={'value': value},
        )


def FirstLetterValidator(value):
    if not value.istitle():
        raise ValidationError(
            _('First letter can only be capitalized'),
            params={'value': value},
        )


class Person(models.Model):
    first_name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        validators=[
            LettersOnlyValidator,
            FirstLetterValidator
        ]
    )
    last_name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        validators=[
            LettersOnlyValidator,
            FirstLetterValidator
        ]
    )
    age = models.IntegerField(
        default=18,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(13),
        ]
    )
    default_city = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        default="New York",
        validators=[
            LettersOnlyValidator,
            FirstLetterValidator
        ]
    )
    theme = models.CharField(
        max_length=7,
        choices=THEME,
        default="Default"
    )
    owner = models.ForeignKey(
        'auth.User',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.first_name.capitalize() + " " + self.last_name.capitalize()

    class Meta:
        ordering = ["last_name"]
        verbose_name_plural = "Users"


class City(models.Model):
    name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        validators=[
            LettersOnlyValidator,
            FirstLetterValidator
        ]
    )
    persons = models.ManyToManyField(
        Person,
        related_name="Cities"
    )

    def __str__(self):
        return self.name.capitalize()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Cities"

