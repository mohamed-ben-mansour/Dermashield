from django.shortcuts import render, redirect
from .forms import RegisterForm,DoctorAppointmentEditForm, PatientAppointmentEditForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as authViews
from .models import CustomUser
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
# Home view
def home0(request):
    return render(request, 'maintemp/home_color.html')
def home(request):
    return render(request, 'maintemp/index.html')
# Signup view
@never_cache
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet to set role
            email = form.cleaned_data.get('email')
            # Set role based on email domain
            if email.endswith('@doctor.tn'):
                user.role = CustomUser.DOCTOR
            else:
                user.role = CustomUser.PATIENT
            user.save()
            login(request, user)  # Log the user in after saving
            return redirect('/users/home')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})

@login_required(login_url='login')
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('home')
    else:
        form = RegisterForm(instance=user)

    return render(request, 'registration/update_user.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})

from django.contrib.auth import views as authViews
from .forms import LoginForm

class CustomLoginView(authViews.LoginView):
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)  # Log out the user if they're already logged in
        return super().dispatch(request, *args, **kwargs)





from .models import Appointment, Note
from .forms import AppointmentForm, NoteForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from .forms import DoctorAppointmentFilterForm
from .models import Notification
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .forms import AppointmentFilterForm


from django.core.paginator import Paginator
from django.utils.timezone import now

@login_required
def doctor_dashboard(request):
    doctor = request.user
    today = now().date()

    # Get the list of patients associated with the doctor through the patient_appointments
    patients = CustomUser.objects.filter(patient_appointments__doctor=doctor).distinct()

    # Get filter form data, passing patients queryset
    filter_form = DoctorAppointmentFilterForm(request.GET or None, patient_queryset=patients)
    
    appointments = Appointment.objects.filter(doctor=doctor)
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('patient'):
            appointments = appointments.filter(patient=filter_form.cleaned_data['patient'])

    # Separate appointments
    appointments_today = appointments.filter(date=today)
    appointments_tomorrow = appointments.filter(date=today + timedelta(days=1))
    past_appointments = appointments.filter(date__lt=today).order_by('-date', '-time')
    upcoming_appointments = appointments.filter(date__gt=today + timedelta(days=1)).order_by('date', 'time')

    # Paginate past and upcoming appointments (5 per page)
    past_page_number = request.GET.get('past_page', 1)
    upcoming_page_number = request.GET.get('upcoming_page', 1)
    past_paginator = Paginator(past_appointments, 5)
    upcoming_paginator = Paginator(upcoming_appointments, 5)

    past_appointments_page = past_paginator.get_page(past_page_number)
    upcoming_appointments_page = upcoming_paginator.get_page(upcoming_page_number)
# Notifications filter logic
    notifications = doctor.notifications.all().order_by('-timestamp')
    notification_type = request.GET.get('notification_type')
    if notification_type:
        if notification_type == 'availability':
        # Adjusting the filter to be more flexible in catching availability messages
            notifications = notifications.filter(
            message__icontains='available'
        )
        elif notification_type == 'modification':
            notifications = notifications.filter(message__icontains='updated the appointment')
        elif notification_type == 'cancellation':
            notifications = notifications.filter(message__icontains='cancelled the appointment')
        elif notification_type == 'deletion':
            notifications = notifications.filter(message__icontains='deleted their account')


    return render(request, 'rdv/doctor_dashboard.html', {
        'filter_form': filter_form,
        'appointments_today': appointments_today,
        'appointments_tomorrow': appointments_tomorrow,
        'past_appointments': past_appointments_page,
        'upcoming_appointments': upcoming_appointments_page,
        'notifications': notifications,
    })




@login_required
def patient_dashboard(request):
    if not request.user.is_patient:
        messages.error(request, "Access restricted to patients.")
        return redirect('login')
    
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    next_week_start = today + timedelta(days=2)
    next_week_end = today + timedelta(days=7)

    # Filter appointments for the patient
    appointments = Appointment.objects.filter(patient=request.user, is_canceled=False)

    # Organize appointments by time periods
    appointments_today = appointments.filter(date=today)
    appointments_tomorrow = appointments.filter(date=tomorrow)
    appointments_next_week = appointments.filter(date__range=(next_week_start, next_week_end))
    future_appointments = appointments.filter(date__gt=next_week_end)
    past_appointments = appointments.filter(date__lt=today)

    # Apply filters if provided in GET request
    filter_form = AppointmentFilterForm(request.GET or None)
    if filter_form.is_valid():
        date = filter_form.cleaned_data.get('date')
        appointment_type = filter_form.cleaned_data.get('appointment_type')

        if date:
            appointments = appointments.filter(date=date)
        if appointment_type:
            appointments = appointments.filter(type=appointment_type)

    # Paginate past and upcoming appointments (5 per page)
    past_page_number = request.GET.get('past_page', 1)
    future_page_number = request.GET.get('future_page', 1)

    past_paginator = Paginator(past_appointments, 5)
    future_paginator = Paginator(future_appointments, 5)

    past_appointments_page = past_paginator.get_page(past_page_number)
    future_appointments_page = future_paginator.get_page(future_page_number)

    # Retrieve unread notifications for the patient
    notifications = request.user.notifications.filter(read=False)

    context = {
        'appointments_today': appointments_today,
        'appointments_tomorrow': appointments_tomorrow,
        'appointments_next_week': appointments_next_week,
        'future_appointments': future_appointments,
        'past_appointments': past_appointments,
        'past_appointments_page': past_appointments_page,
        'future_appointments_page': future_appointments_page,
        'filter_form': filter_form,
        'notifications': notifications,
    }

    return render(request, 'rdv/patient_dashboard.html', context)

from django.utils import timezone
from datetime import date,time,datetime, timedelta
from django.utils.timezone import now
from .models import Notification


from .utils import generate_time_slots
from django.http import JsonResponse


@login_required
def create_appointment(request):
    today_date = date.today().isoformat()
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    NoteFormSet = inlineformset_factory(Appointment, Note, form=NoteForm, extra=1, can_delete=True)

    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        selected_time = request.POST.get('selected_time')

        if selected_time:
            selected_time = selected_time.split(' - ')[0]  # Extract start time

        form = AppointmentForm(request.POST)
        formset = NoteFormSet(request.POST)

        if form.is_valid() and formset.is_valid() and selected_date and selected_time:
            appointment = form.save(commit=False)
            appointment.doctor = request.user
            appointment.date = selected_date
            appointment.time = selected_time
            appointment.save()

            formset.instance = appointment
            formset.save()

            messages.success(request, "Appointment created successfully!")
            return redirect('doctor_dashboard')

        messages.error(request, "Please fill all required fields and select a valid time slot.")
    else:
        form = AppointmentForm()
        formset = NoteFormSet()

    selected_date = datetime.today().date()
    start_time = datetime.combine(selected_date, time(8, 0))
    end_time = datetime.combine(selected_date, time(17, 0))
    slots = generate_time_slots(start_time, end_time)

    slots_table = []
    for slot_start, slot_end in slots:
        slots_table.append({
            "time": f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}",
            "available": True,
        })

    return render(request, 'rdv/create_appointment.html', {
        'form': form,
        'formset': formset,
        'slots_table': slots_table,
        'weekdays': weekdays,
        'today_date': today_date,
    })


@login_required
def get_slots(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({"slots": []})

    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    slots = generate_time_slots(date_obj)

    # Check availability for each slot
    available_slots = []
    for slot_start, slot_end in slots:
        is_available = not Appointment.objects.filter(
            doctor=request.user,
            date=date_obj,
            time__gte=slot_start.time(),
            time__lt=slot_end.time()
        ).exists()

        available_slots.append({
            "start": slot_start.strftime('%H:%M'),
            "end": slot_end.strftime('%H:%M'),
            "available": is_available
        })

    return JsonResponse({"slots": available_slots})




def create_notification(recipient, message):
    """Helper function to create a notification."""
    Notification.objects.create(
        recipient=recipient,
        message=message,
        timestamp=now(),
    )

@login_required
def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    NoteFormSet = inlineformset_factory(Appointment, Note, form=NoteForm, extra=1, can_delete=True)

    if request.user.is_doctor:
        form = DoctorAppointmentEditForm(request.POST or None, instance=appointment)
        formset = NoteFormSet(request.POST or None, instance=appointment)
    elif request.user.is_patient:
        form = PatientAppointmentEditForm(request.POST or None, instance=appointment)
        formset = None  # Patients cannot edit notes
    else:
        return redirect('home')

    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        selected_time = request.POST.get('selected_time')

        # Extract the start time
        if selected_time:
            selected_time = selected_time.split(' - ')[0]

        if form.is_valid() and (not formset or formset.is_valid()) and selected_date and selected_time:
            # Update the appointment's date and time
            appointment.date = selected_date
            appointment.time = selected_time
            form.save()
            if formset:
                formset.save()

            # Create notifications
            message = f"Appointment on {selected_date} at {selected_time} was updated."
            if request.user.is_doctor:
                # Notify patient
                create_notification(appointment.patient, f"Your doctor updated your appointment. {message}")
            elif request.user.is_patient:
                # Notify doctor
                create_notification(appointment.doctor, f"Your patient updated the appointment. {message}")

            # Notify both parties (optional, if both should always be notified regardless of editor)
            create_notification(appointment.doctor, message)
            create_notification(appointment.patient, message)

            messages.success(request, "Appointment updated successfully!")
            return redirect('appointment_detail', pk=pk)

        messages.error(request, "Please fill all required fields and select a valid time slot.")

    # Prepare data for the calendar
    selected_date = appointment.date
    start_time = datetime.combine(selected_date, time(8, 0))
    end_time = datetime.combine(selected_date, time(17, 0))
    slots = generate_time_slots(start_time, end_time)

    slots_table = []
    for slot_start, slot_end in slots:
        slots_table.append({
            "time": f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}",
            "available": True,
        })

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    return render(request, 'rdv/edit_appointment.html', {
        'form': form,
        'note_formset': formset,
        'appointment': appointment,
        'slots_table': slots_table,
        'weekdays': weekdays,
        'today_date': selected_date.isoformat(),
    })






@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.user != appointment.doctor and request.user != appointment.patient:
        messages.error(request, "Access denied.")
        return redirect('login')

    # Notify the other party about the cancellation
    if request.user == appointment.patient:
        message = f"{request.user.username} canceled their appointment on {appointment.date} at {appointment.time}."
        Notification.objects.create(
            recipient=appointment.doctor,
            message=message,
            timestamp=now()
        )
    elif request.user == appointment.doctor:
        message = f"{request.user.username} canceled your appointment on {appointment.date} at {appointment.time}."
        Notification.objects.create(
            recipient=appointment.patient,
            message=message,
            timestamp=now()
        )

    appointment.is_canceled = True
    appointment.save()
    messages.success(request, "Appointment canceled successfully.")
    return redirect('doctor_dashboard' if request.user.is_doctor else 'patient_dashboard')

@login_required
def appointment_detail(request, pk):
    # Get the appointment or return a 404 if not found
    appointment = get_object_or_404(Appointment, id=pk)

    # Check if the logged-in user is the assigned doctor or patient for this appointment
    if request.user == appointment.doctor or request.user == appointment.patient:
        # Define notes based on visibility; patient only sees visible notes
        notes = appointment.notes.all() if request.user == appointment.doctor else appointment.notes.filter(visible_to_patient=True)
        can_edit = request.user == appointment.doctor  # Allow full edit access for doctors only

        # Render the appointment details page
        return render(request, 'rdv/appointment_detail.html', {
            'appointment': appointment,
            'notes': notes,
            'can_edit': can_edit
        })
    else:
        # Redirect unauthorized users to the home page or their dashboard
        messages.error(request, "Access denied.")
        return redirect('/user/home')

@login_required
def toggle_availability(request):
    if request.method == 'POST' and request.user.is_patient:
        request.user.bookable = not request.user.bookable
        request.user.save()
        # Notify all doctors about the patient's availability change
        message = f"{request.user.username} is now {'available' if request.user.bookable else 'not available'} for booking."
        doctors = CustomUser.objects.filter(role=CustomUser.DOCTOR)
        for doctor in doctors:
            Notification.objects.create(recipient=doctor, message=message)

        messages.success(request, "Availability updated successfully.")
    return redirect('patient_dashboard')






@receiver(post_delete, sender=CustomUser)
def create_account_deletion_notification(sender, instance, **kwargs):
    if instance.role == CustomUser.PATIENT:
        message = f"{instance.username} has deleted their account."
        Notification.objects.create(recipient=instance.doctor, message=message)
    elif instance.role == CustomUser.DOCTOR:
        patients = Appointment.objects.filter(doctor=instance).values_list('patient', flat=True).distinct()
        message = f"{instance.username} (your doctor) has deleted their account."
        for patient_id in patients:
            Notification.objects.create(recipient_id=patient_id, message=message)



@login_required
def mark_notifications_read(request):
    if request.method == 'POST':
        # Update only the current user's notifications
        request.user.notifications.filter(read=False).update(read=True)
        messages.success(request, "All notifications marked as read.")
    return redirect('doctor_dashboard' if request.user.is_doctor else 'patient_dashboard')






from django.http import JsonResponse

@login_required
def paginate_appointments(request):
    doctor = request.user
    today = now().date()

    # Determine type of appointments to paginate
    appointment_type = request.GET.get('type', 'past')  # 'past' or 'upcoming'
    page = int(request.GET.get('page', 1))

    appointments = Appointment.objects.filter(doctor=doctor)

    if appointment_type == 'past':
        appointments = appointments.filter(date__lt=today).order_by('-date', '-time')
    elif appointment_type == 'upcoming':
        appointments = appointments.filter(date__gt=today + timedelta(days=1)).order_by('date', 'time')

    # Paginate appointments
    paginator = Paginator(appointments, 5)
    appointments_page = paginator.get_page(page)

    # Serialize appointments for JSON response
    appointment_data = [
        {
            'id': appointment.id,
            'type': appointment.type,
            'date': appointment.date.isoformat(),
            'time': appointment.time,
            'patient': appointment.patient.username
        } for appointment in appointments_page
    ]

    return JsonResponse({
        'appointments': appointment_data,
        'has_next': appointments_page.has_next(),
        'has_previous': appointments_page.has_previous(),
        'next_page_number': appointments_page.next_page_number() if appointments_page.has_next() else None,
        'previous_page_number': appointments_page.previous_page_number() if appointments_page.has_previous() else None,
    })




