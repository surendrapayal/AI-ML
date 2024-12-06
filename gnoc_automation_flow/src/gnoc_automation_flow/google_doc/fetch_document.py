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

def fetch_google_doc_content(doc_id):
    """Fetch the content of a Google Doc."""
    creds = authenticate_google_api()
    service = build("docs", "v1", credentials=creds)

    # Fetch the document
    document = service.documents().get(documentId=doc_id).execute()

    # Parse the content
    content = ""
    for element in document.get("body", {}).get("content", []):
        if "paragraph" in element:
            for text_element in element["paragraph"]["elements"]:
                content += text_element.get("textRun", {}).get("content", "")

    return content

if __name__ == "__main__":
    # Replace with your Google Doc ID
  #  doc_id = "1x_-1k97cDjWvE2AU9BjZOgcMPdYwxjze"
    doc_id ="1da2d_XwwNOrwTXp31XsBz6geBHsQ1XMX"
    doc_content = fetch_google_doc_content(doc_id)
    print("Google Doc Content:")
    print(doc_content)
