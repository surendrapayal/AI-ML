from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
# Path to your credentials JSON file
CREDENTIALS_FILE = "C:\\Users\\Test\\Desktop\\CrewAI\\AI-ML\\gnoc_automation_flow\\credentials.json"
SCOPES = ["https://www.googleapis.com/auth/documents.readonly","https://www.googleapis.com/auth/documents"]

def authenticate_google_api():
    """Authenticate and return Google API credentials."""
    creds = None
    # Load existing token or create a new one
    if os.path.exists("google_doc_token.json"):
        creds = Credentials.from_authorized_user_file("google_doc_token.json", SCOPES)
    if not creds or not creds.valid:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("google_doc_token.json", "w") as token_file:
            token_file.write(creds.to_json())
    return creds

def list_google_docs():
    """List all Google Docs in Google Drive."""
    creds = authenticate_google_api()  # Add your credentials handling here
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q="mimeType='application/vnd.google-apps.document'",
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])
    if not items:
        print("No Google Docs found.")
    else:
        print("Google Docs in your Drive:")
        for item in items:
            print(f"{item['name']} (ID: {item['id']}, MIME Type: {item['mimeType']})")

list_google_docs()
