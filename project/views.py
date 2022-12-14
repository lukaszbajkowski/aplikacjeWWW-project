import urllib

from django.db.migrations import serializer
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.utils import json

from .serializers import *
from .forms import *
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

for user in User.objects.all():
    Token.objects.get_or_create(user=user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@api_view(['GET', 'PUT'])
@authentication_classes([
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def person_list(request):
    if request.method == 'GET':
        osoba = Person.objects.filter(owner_id=request.user.id)
        serializer = PersonSerializer(osoba, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def person_detail(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        person = Person.objects.get(pk=pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)


@api_view(['POST'])
def person_new(request):
    form = UserForm(request.POST)
    if form.is_valid():
        person = form.cleaned_data
        new_person = Person(
            first_name=person['first_name'],
            last_name=person['last_name'],
            age=person['age'],
            default_city=person['default_city'],
            theme=person['theme'],
            owner=request.user.id
        )
        new_person.save()
        return HttpResponseRedirect(f'/person/{new_person.id}')
    else:
        return HttpResponse('Invalid form, please try again.')


@api_view(['PUT'])
@authentication_classes([
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def person_update(request, pk):
    if request.user.is_authenticated:
        try:
            person = Person.objects.get(pk=pk, owner_id=request.user.id)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            form = EditUserForm(request.POST)
            person_copy = person.copy()
            if form.is_valid():
                update_person = form.cleaned_data
                if person.first_name != update_person['first_name']:
                    person.first_name = update_person['first_name']
                    person.save()
                if person.last_name != update_person['last_name']:
                    person.last_name = update_person['last_name']
                    person.save()
                if person.default_city != update_person['default_city']:
                    person.default_city = update_person['default_city']
                    person.save()
                if person.theme != update_person['theme']:
                    person.theme = update_person['theme']
                    person.save()
                return HttpResponseRedirect(f'/person/{person.id}')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                person = person_copy
                person.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return HttpResponse('You\'re not authorized')


@api_view(['DELETE'])
@authentication_classes([
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def person_delete(request, pk):
    if request.user.is_authenticated:
        try:
            person = Person.objects.get(pk=pk, owner=request.user.id)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'DELETE':
            Person.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return HttpResponseRedirect('You\'re not authorized')


@api_view(['GET'])
@authentication_classes([
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def city_list(request):
    if request.method == 'GET':
        city = City.objects.all()
        serializer = CitySerializer(city, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def city_detail(request, pk):
    try:
        city = City.objects.get(pk=pk)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        city = City.objects.get(pk=pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def city_update(request, pk):
    if request.user.is_authenticated:
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            form = EditCityForm(request.POST)
            city_copy = city.copy()
            if form.is_valid():
                update_city = form.cleaned_data
                if city.persons != update_city['persons']:
                    city.persons = update_city['persons']
                    city.save()
                return HttpResponseRedirect(f'/city/{city.id}')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                city = city_copy
                city.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return HttpResponse('You\'re not authorized')


@api_view(['DELETE'])
@authentication_classes([
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def city_delete(request, pk):
    if request.user.is_authenticated:
        try:
            city = City.objects.get(pk=pk, owner=request.user.id)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'DELETE':
            City.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return HttpResponseRedirect('You\'re not authorized')


@api_view(['POST'])
def city_new(request):
    form = CityForm(request.POST)
    if form.is_valid():
        city = form.cleaned_data
        new_city = City(
            name=city['name'],
            persons=city['persons'],
        )
        new_city.save()
        return HttpResponseRedirect(f'/city/{new_city.id}')
    else:
        return HttpResponse('Invalid form, please try again.')


def city_search(request):
    if request.method == 'POST':

        city = request.POST['city']
        url = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q='
            + city +
            '&units=metric&appid=cd4415a99345841edbb9040348e3f2d6').read()
        r = json.loads(url)

        city_weather = {
            'country': str(r['name']),
            'temp': str(r["main"]['temp']),
            'pressure': str(r['main']["pressure"]),
            'humidity': str(r['main']['humidity']),
            'main': str(r["weather"][0]['main']),
            'description': str(r["weather"][0]['description']),
            'icon': r["weather"][0]['icon'],
            'city': city
        }
    else:
        city_weather = {}
    # return render(request, 'weather.html', city_weather)


def city_show_weather(request):
    if request.method == 'POST':
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=cd4415a99345841edbb9040348e3f2d6'
        cities = City.objects.all()
        weather_data = []

        for city in cities:
            r = request.get(url.format(city)).json()

            city_weather = {
                'country': str(r['name']),
                'temp': str(r["main"]['temp']),
                'pressure': str(r['main']["pressure"]),
                'humidity': str(r['main']['humidity']),
                'main': str(r["weather"][0]['main']),
                'description': str(r["weather"][0]['description']),
                'icon': r["weather"][0]['icon'],
                'city': city
            }

        context = {'weather_data': weather_data}
        # return render(request, 'weather2.html', context)


@api_view(['PUT'])
@authentication_classes([
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def city_add_to_favorite(request, pk):
    if request.user.is_authenticated:
        try:
            city = City.objects.get(pk=pk, owner=request.user.id)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            city.persons = request.user.id
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return HttpResponseRedirect('You\'re not authorized')
