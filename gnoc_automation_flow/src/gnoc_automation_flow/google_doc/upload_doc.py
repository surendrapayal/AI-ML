from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

# Path to your credentials JSON file
CREDENTIALS_FILE = "C:\\Users\\Test\\Desktop\\CrewAI\\AI-ML\\gnoc_automation_flow\\credentials.json"
SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"]

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

def create_beautiful_doc():
    """Create a beautiful Google Doc with formatted content."""
    creds = authenticate_google_api()
    docs_service = build("docs", "v1", credentials=creds)

    # Create a new Google Doc
    doc_body = {"title": "Beautiful Google Doc"}
    document = docs_service.documents().create(body=doc_body).execute()
    doc_id = document.get("documentId")
    print(f"Google Doc created: https://docs.google.com/document/d/{doc_id}")

    # Add formatted content
    requests = [
        # Add a title
        {"insertText": {"location": {"index": 1}, "text": "Welcome to Your Beautiful Document!\n\n"}},
        {"updateTextStyle": {
            "range": {"startIndex": 1, "endIndex": 34},
            "textStyle": {"bold": True, "fontSize": {"magnitude": 20, "unit": "PT"}},
            "fields": "bold,fontSize"
        }},
        # Add a subtitle
        {"insertText": {"location": {"index": 35}, "text": "This document was created using Python.\n\n"}},
        {"updateTextStyle": {
            "range": {"startIndex": 35, "endIndex": 78},
            "textStyle": {"italic": True, "foregroundColor": {"color": {"rgbColor": {"red": 0.1, "green": 0.5, "blue": 0.8}}}},
            "fields": "italic,foregroundColor"
        }},
        # Add a bullet point list
        {"insertText": {"location": {"index": 79}, "text": "Key Features:\n"}},
        {"insertText": {"location": {"index": 92}, "text": "- Automated creation\n- Beautiful formatting\n- Python-powered\n"}},
        {"createParagraphBullets": {
            "range": {"startIndex": 92, "endIndex": 146},
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }}
    ]

    docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

    print(f"Formatted content added to Google Doc: https://docs.google.com/document/d/{doc_id}")

    return doc_id

if __name__ == "__main__":
    create_beautiful_doc()
