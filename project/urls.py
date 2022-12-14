from django.urls import path, include
from . import views

urlpatterns = [
    path('person/', views.person_list),
    path('person/<int:pk>/', views.person_detail),
    path('person/update/<int:pk>/', views.person_update),
    path('person/delete/<int:pk>/', views.person_delete),
    path('person/new/', views.person_new),
    path('city/', views.city_list),
    path('city/<int:pk>/', views.city_detail),
    path('city/update/<int:pk>/', views.city_update),
    path('city/delete/<int:pk>/', views.city_delete),
    path('city/search/', views.city_search),
    path('city/show/', views.city_show_weather),
    path('city/add_to_favorite', views.city_add_to_favorite),
    path('login/', include('rest_framework.urls'))
]
