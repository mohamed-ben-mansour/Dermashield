from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Appointment,Note

class CustomUserAdmin(UserAdmin):
    # Customizing how the user list will appear in the admin interface
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name','profile_picture', 'role', 'date_of_birth', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'role']
    search_fields = ['username', 'email']
    ordering = ['username']

    # Customizing the fieldsets (displayed fields in the user change form)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','profile_picture', 'email', 'role', 'date_of_birth', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Customizing the add_fieldsets (fields shown during user creation)
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name','profile_picture', 'email', 'role', 'date_of_birth', 'phone_number')}),
    )

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment)
