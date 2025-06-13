from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from oauth2_provider.views.generic import ProtectedResourceView
from .models import Event
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import pytz

from django.views import View  # Import Django's base View class

class CalendarView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is your calendar view. Google Calendar integration is working!")


def fetch_events(request):
    try:
        # Authenticate with Google Calendar API
        creds = Credentials.from_authorized_user_file('token.json')
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Build Google Calendar API service
        service = build('calendar', 'v3', credentials=creds)

        # Retrieve events from Google Calendar
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events_data = events_result.get('items', [])

        print(f"Fetched events: {events_data}")  # Log fetched events

        # Save events to the database
        for event_data in events_data:
            start_time = event_data['start'].get('dateTime', event_data['start'].get('date'))
            end_time = event_data['end'].get('dateTime', event_data['end'].get('date'))
            start_time = datetime.datetime.fromisoformat(start_time)
            end_time = datetime.datetime.fromisoformat(end_time)
            # Convert to UTC timezone
            start_time = pytz.utc.localize(start_time)
            end_time = pytz.utc.localize(end_time)
            # Save or update the event in the database
            Event.objects.update_or_create(
                start_time=start_time,
                end_time=end_time,
                defaults={'summary': event_data.get('summary', '')}
            )

        # Retrieve events from the database and display
        events = Event.objects.all()
        context = {'events': events}
        return render(request, 'calendar_integration/calendar_events.html', context)

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
