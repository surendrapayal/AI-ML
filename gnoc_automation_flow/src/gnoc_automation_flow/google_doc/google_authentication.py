from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

# Scopes for Google APIs
SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive.file"]
CREDENTIALS_FILE = "C:\\Users\\Test\\Desktop\\CrewAI\\AI-ML\\gnoc_automation_flow\\credentials.json"
def authenticate_google_api():
    """Authenticate and return credentials."""
    creds = None
    # Check if token.json exists
    if os.path.exists("google_doc_token.json"):
        creds = Credentials.from_authorized_user_file("google_doc_token.json", SCOPES)

    # If no valid credentials are available, log in again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("google_doc_token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return creds

authenticate_google_api()