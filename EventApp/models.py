#models

from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

from main.models import CustomUser

from django.shortcuts import render
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model




from django.apps import apps


class Event(models.Model):
    id = models.AutoField(primary_key=True)  # Remove default=1
    event_title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(5, "Title must be at least 5 characters long.")]
    )
    EVENT_TYPES = [
        ('Health Screening', 'Health Screening'),
        ('Wellness Workshop', 'Wellness Workshop'),
        ('Community Talk', 'Community Talk'),
        ('Awareness Campaign', 'Awareness Campaign'),
        ('Fitness Class', 'Fitness Class'),
        ('Support Group', 'Support Group'),
    ]
    event_Type = models.CharField(
        max_length=255,
        choices=EVENT_TYPES,
        help_text="Choose event type from the list."
    )
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(
        max_length=255,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9\s,.-]*$',
            message="Location should not contain special characters."
        )]
    )
    affiche = models.FileField(
        upload_to='files/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg']),
        ]
    )
    created_at = models.DateTimeField('Creation Date', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Set the new_event flag for all users
        User = get_user_model()
        User.objects.update(new_event=True)
        
    def clean(self):
        super().clean()
        
        # Validate end date is after start date
        def clean(self):
           super().clean()  # Call the base class clean method
           if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

        # Validate affiche file size (e.g., max 5MB)
        if self.affiche and self.affiche.size > 5 * 1024 * 1024:  # 5MB limit
            raise ValidationError("File size should not exceed 5MB.")
    
    
        
    
class Seat(models.Model):
    event = models.ForeignKey(Event, related_name='seats', on_delete=models.CASCADE)
    row = models.CharField(max_length=1)  # Example: 'A', 'B', 'C'
    number = models.IntegerField()
    is_booked = models.BooleanField(default=False)          

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)  
   
    
    

      
    
    
