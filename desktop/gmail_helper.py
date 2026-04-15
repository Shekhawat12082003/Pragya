"""
Gmail integration via Gmail API.
Setup: https://developers.google.com/gmail/api/quickstart/python
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""
import os
import base64
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'gmail_token.json')
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
                return None, "Gmail credentials not found. Add gmail_credentials.json to desktop folder."
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds), None

def read_emails(count=3):
    service, err = _get_service()
    if err: return err
    try:
        results = service.users().messages().list(userId='me', maxResults=count, labelIds=['INBOX', 'UNREAD']).execute()
        messages = results.get('messages', [])
        if not messages:
            return "No unread emails."
        summaries = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id'], format='metadata',
                metadataHeaders=['From', 'Subject']).execute()
            headers = {h['name']: h['value'] for h in m['payload']['headers']}
            summaries.append(f"From {headers.get('From','?')}: {headers.get('Subject','No subject')}")
        return f"{len(summaries)} unread emails. " + ". ".join(summaries)
    except Exception as e:
        return f"Could not read emails: {e}"

def send_email(to, subject, body):
    service, err = _get_service()
    if err: return err
    try:
        msg = MIMEText(body)
        msg['to'] = to
        msg['subject'] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw}).execute()
        return f"Email sent to {to}."
    except Exception as e:
        return f"Failed to send email: {e}"
