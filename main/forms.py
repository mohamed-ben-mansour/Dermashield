# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .models import Appointment, Note

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

class LoginForm(AuthenticationForm):
    captcha = CaptchaField()


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'email','profile_picture', 'date_of_birth']
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
#         }




class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    profile_picture = forms.FileField(required=False)  # Add the profile_picture field
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name','profile_picture', 'date_of_birth', 'password1', 'password2']

    def clean_email(self):
        # Get email and check the domain
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError(_("Email is required"))
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_("Password must contain at least one number."))
        if not any(char.isalpha() for char in password):
            raise ValidationError(_("Password must contain at least one letter."))
        return password

from django.contrib.auth import get_user_model

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=User.objects.filter(role='patient', bookable=True), 
        required=True
    )
    type = forms.ChoiceField(choices=Appointment.APPOINTMENT_TYPES, required=True)  # Assuming this is defined in your model

    class Meta:
        model = Appointment
        fields = ['patient', 'type'] 

class NoteForm(forms.ModelForm):
    visible_to_patient = forms.BooleanField(required=False)

    class Meta:
        model = Note
        fields = ['content', 'visible_to_patient']

class DoctorAppointmentEditForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'type']  # Remove date and time

class PatientAppointmentEditForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = []  # Patients only update date and time via the calendar



class AppointmentFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    type = forms.ChoiceField(
        choices=[('', 'All Types')] + Appointment.APPOINTMENT_TYPES,  
        required=False
    )


class DoctorAppointmentFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Accept a 'patient_queryset' argument to restrict patient options
        patient_queryset = kwargs.pop('patient_queryset', CustomUser.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = patient_queryset

    patient = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(),  # Default empty queryset
        required=False,
        empty_label="All Patients"
    )

 
    