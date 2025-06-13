from django.urls import path
from .views import *
from . import views 
app_name = 'events'

urlpatterns = [
    path('list/', EventListView.as_view(), name='event_list'),
    path('details/<int:pk>', EventDetailView.as_view(), name='event_details'),

    #path('index/',EventListView.as_view(), name='index'),
    path('event/<int:event_id>/', views.event_seating, name='event_seating'),
    path('book-seat/<int:seat_id>/', views.book_seat, name='book_seat'),

]