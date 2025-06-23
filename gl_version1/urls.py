"""
URL configuration for gl_version1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include 
from django.conf import settings
from django.conf.urls.static import static
from main import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('main.urls')),
    path('tips/',include('tips.urls')),
    path('events/',include('EventApp.urls')),
    path('',views.home0),
    path('feedback/', include('feedback.urls')),
    path('forums/', include('forum.urls')),
    path('user/dashboard',include('main.urls')),
    path('captcha/', include('captcha.urls')),
    path('calories/', include('counter.urls')),
    path('model/', include('model.urls')),
    path('chatbot/', include('chatbot.urls')),  # Add this line
    path('calendar/', include('calendar_integration.urls')),
    # path('emotion/', include('emotion_detection.urls')),

    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

