from django.contrib import admin
from .models import *


class PersonInline(admin.TabularInline):
    model = City.persons.through
    verbose_name_plural = "Favorite cities"


class PersonAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'age',
        'default_city'
    ]
    list_filter = [
        'last_name',
        'first_name',
        "age",
        "default_city"
    ]
    fieldsets = [
        ('User information', {'fields': [
            'first_name',
            'last_name',
            'age'
        ]}),
        ('Default City', {'fields': [
            'default_city'
        ]}),
        ('Other information', {'fields': [
            'theme'
        ]}),
    ]
    search_fields = [
        'default_city',
        'first_name',
        'last_name'
    ]
    inlines = [
        PersonInline,
    ]


class CityAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    list_filter = [
        'name'
    ]
    fieldsets = [
        ('Name of the city', {'fields': [
            'name'
        ]}),
    ]
    inlines = [
        PersonInline,
    ]
    search_fields = [
        'name',
    ]
    exclude = ['persons']


admin.site.register(City, CityAdmin)
admin.site.register(Person, PersonAdmin)
