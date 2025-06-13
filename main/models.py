# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    PATIENT = 'patient'
    new_event = models.BooleanField(default=False)


    profile_picture = models.FileField(upload_to='profile_pictures/', blank=True, null=True)
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
    ]
    
    role = models.CharField(
        max_length=7,
        choices=ROLE_CHOICES,
        default=PATIENT,
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Set staff and superuser status based on role
        if self.role == self.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)
    bookable = models.BooleanField(default=False)
    # Helper methods
    @property
    def is_doctor(self):
        return self.role == self.DOCTOR

    def is_patient(self):
        return self.role == self.PATIENT

    def is_admin(self):
        return self.role == self.ADMIN


from django.contrib.auth import get_user_model

User = get_user_model()

class Appointment(models.Model): 
    APPOINTMENT_TYPES = [
        ('test', 'Test'),
        ('visit', 'Visit'),
        ('operation', 'Operation'),
    ]

    doctor = models.ForeignKey(
        User,
        related_name='doctor_appointments',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'}
    )
    patient = models.ForeignKey(
        User,
        related_name='patient_appointments',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'}
    )
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=10, choices=APPOINTMENT_TYPES)
    is_canceled = models.BooleanField(default=False)
    summary = models.CharField(max_length=255, blank=True, null=True)  # For Google Calendar event summary
    google_event_id = models.CharField(max_length=255, blank=True, null=True)  # Google Calendar event ID

    def __str__(self):
        return f"{self.type} on {self.date} at {self.time} between {self.doctor.username} and {self.patient.username}"


class Note(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='notes', on_delete=models.CASCADE)
    content = models.TextField()
    visible_to_patient = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.appointment}"

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"


class AppointmentRequest(models.Model):
    patient = models.ForeignKey(User, related_name="appointment_requests", on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    requested_at = models.DateTimeField(auto_now_add=True)

    def is_conflicting(self):
        # Logic to check if the requested time conflicts with any doctor's appointments
        return Appointment.objects.filter(
            date=self.date,
            time=self.time,
        ).exists()


