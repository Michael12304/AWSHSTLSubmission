from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport import Request
import datetime
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow

def exchange_google_refresh_for_token(client_id: str, client_secret: str, refresh_token: str) -> dict:

    credentials = Credentials(
        None,  # No access token since we're refreshing
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )

    # Force a refresh of the credentials
    credentials.refresh(Request())

    return {
        'access_token': credentials.token,
        'expires_in': credentials.expiry.timestamp() - datetime.datetime.now().timestamp(),
        'token_type': 'Bearer'
    }

def exchange_google_code_for_token(client_id: str, client_secret: str, code: str, redirect_uri: str) -> dict:

    # Create flow instance to help with token request
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=redirect_uri
    )

    # Exchange code for tokens
    flow.fetch_token(code=code)
    credentials = flow.credentials

    return {
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'expires_in': credentials.expiry.timestamp() - datetime.datetime.now().timestamp(),
        'token_type': 'Bearer'
    }

def createGoogleCalendarEvent(accessToken : str, 
                                 summary : str, 
                                 description : str, 
                                 startTime : datetime.datetime, 
                                 endTime : datetime.datetime, 
                                 invitees : list[str] = None,
                                 timezone : str = 'America/Toronto'):
    # Create credentials object from the access token
    creds = Credentials(accessToken)

    # Build the Google Calendar service
    service = build('calendar', 'v3', credentials=creds)

    # Create the event body
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': startTime.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': endTime.isoformat(),
            'timeZone': timezone,
        },
    }

    # Add invitees if provided
    if invitees:
        event['attendees'] = [{'email': email} for email in invitees]

    # Insert the event
    event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
    print(f'Event created: {event.get("htmlLink")}')