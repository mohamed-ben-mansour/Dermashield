from django.urls import path
from django.contrib.auth import views as authViews
from . import views
from .views import CustomLoginView,update_profile,profile
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('home/', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),


    path('logout/', authViews.LogoutView.as_view(), name='logout'),
    path('password_reset/', authViews.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirmm.html'), name='password_reset_confirm'),
    path('password_reset/done/', authViews.PasswordResetDoneView.as_view(template_name='registration/password_reset_doone.html'), name='password_reset_done'),
    path('password-reset-complete/', authViews.PasswordResetCompleteView.as_view(template_name='registration/password_reset_completee.html'), name='password_reset_complete'),


    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('appointment/create/', views.create_appointment, name='create_appointment'),
    path('appointment/<int:pk>/edit/', views.edit_appointment, name='edit_appointment'),
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('toggle_availability/', views.toggle_availability, name='toggle_availability'),
    path('appointment/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('api/appointments/', views.paginate_appointments, name='paginate_appointments'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
