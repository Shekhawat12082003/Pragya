"""
Google Calendar integration.
Uses same credentials as Gmail.
pip install google-api-python-client google-auth-oauthlib
"""
import os
from datetime import datetime, timedelta, timezone

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'calendar_token.json')
CREDS_FILE = os.path.join(os.path.dirname(__file__), 'gmail_credentials.json')

def _get_service():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                return None, "Calendar credentials not found."
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds), None

def get_today_events():
    service, err = _get_service()
    if err: return err
    try:
        now = datetime.now(timezone.utc)
        end = now + timedelta(days=1)
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat(),
            timeMax=end.isoformat(),
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        if not events:
            return "No events today."
        summaries = []
        for e in events:
            start = e['start'].get('dateTime', e['start'].get('date', ''))
            if 'T' in start:
                t = datetime.fromisoformat(start).strftime('%I:%M %p')
            else:
                t = "All day"
            summaries.append(f"{e['summary']} at {t}")
        return f"{len(summaries)} events today: " + ", ".join(summaries)
    except Exception as e:
        return f"Could not fetch calendar: {e}"
