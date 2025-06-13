from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('fetch-events/', views.fetch_events, name='fetch_events'),
]