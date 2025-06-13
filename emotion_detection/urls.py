from django.urls import path
from . import views

urlpatterns = [
    path('video_feed/', views.video_feed, name='video_feed'),  # Route for the video stream
    path('live_emotion_detection/', views.live_emotion_detection, name='live_emotion_detection'),  # Route for the live emotion page
]
