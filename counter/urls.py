from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_calories, name='home_calories'),
]
