from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import admin_only_view

urlpatterns = [
    # Main page listing tips
    path('', views.main_page, name='main_page'),
    
    # Update a tip
    path('update/<int:pk>/', views.tip_update, name='tip_update'),
    
    # Delete a tip
    path('delete/<int:pk>/', views.tip_delete, name='tip_delete'),
    
    # Admin view for uploading tips (admin-only access)
    path('admin_upload/', admin_only_view, name='admin_upload'),
    
    # Detail page for a specific tip
    path('tips/<int:tip_id>/', views.tip_detail, name='tip_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
