from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import admin_only_view
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('update/<int:pk>/', views.tip_update, name='tip_update'),
    path('delete/<int:pk>/', views.tip_delete, name='tip_delete'),
     path('admin_upload/', admin_only_view, name='admin_upload'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
