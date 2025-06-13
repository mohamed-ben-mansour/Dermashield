from django.core.management.base import BaseCommand
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from main.models import Appointment
from datetime import datetime
import pytz
import os

class Command(BaseCommand):
    help = "Fetch events from Google Calendar and store them in the database"

    def handle(self, *args, **kwargs):
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('calendar', 'v3', credentials=creds)

        now = datetime.utcnow().isoformat() + 'Z'  # UTC 'Z' time format
        events_result = service.events().list(
            calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        for event in events:
            event_id = event.get('id')
            summary = event.get('summary', 'No Summary')
            start_time = event['start'].get('dateTime')
            end_time = event['end'].get('dateTime')

            if start_time and end_time:
                start_dt = datetime.fromisoformat(start_time).astimezone(pytz.utc)
                # Check if the event already exists
                if not Appointment.objects.filter(google_event_id=event_id).exists():
                    Appointment.objects.create(
                        date=start_dt.date(),
                        time=start_dt.time(),
                        summary=summary,
                        google_event_id=event_id
                    )

        self.stdout.write(self.style.SUCCESS('Successfully fetched events from Google Calendar'))
