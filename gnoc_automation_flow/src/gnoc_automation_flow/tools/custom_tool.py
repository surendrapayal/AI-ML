import json
from email.mime.multipart import MIMEMultipart

import requests
from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool
from dotenv import load_dotenv
from jira import JIRA
from crewai_tools import tool
from pypdf import PdfReader
from model.model_classes import MyCustomJiraToolInput, EmailTemplate
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceCredential
import base64
import pytz

# loading variables from .env file
load_dotenv()
# Jira credentials and endpoint
jira_url = os.getenv("JIRA_URL")
# jira_url = 'https://rahuluraneai.atlassian.net/'
api_token = os.getenv("JIRA_API_TOKEN")  # You can generate this from your Atlassian account
email = os.getenv("FROM_EMAIL")  # Your Jira login email
project_key = os.getenv("JIRA_PROJECT_KEY")  # Replace with your Jira project key
issue_type = "Bug"  # Issue type (Bug in this case)
status_page_url = os.getenv("STATUS_PAGE_URL")
status_page_headers = {
    "Authorization": f"OAuth {os.getenv("STATUS_API_TOKEN")}",
    "Content-Type": "application/json"
}

@tool
def pdf_reader():
    "Read the pdf file and return the content of the file"
    # reader = PdfReader("C:\\MyData\\AI-ML\\gnoc_automation_flow\\Priority.pdf")
    reader = PdfReader(os.getenv("PRIORITY_FILE"))
    text=""
    for page in range(len(reader.pages)):
        pageObj = reader.pages[page]
        text+=pageObj.extract_text()
    return text

@tool
def custom_jira_tool(custom_input: MyCustomJiraToolInput):
    """
        Create a Jira ticket with the given details.
        if this method is executed then stop
    """
    print(f"priority inside jira tool:- {custom_input.priority}")
    print(f"summary inside jira tool:- {custom_input.summary}")
    print(f"description inside jira tool:- {custom_input.description}")
    # Create the Jira issue payload (JSON body)
    issue_data = {
         'project': {
             'id': '10000'
            },
            'summary': f'{custom_input.priority} - {custom_input.summary}',
            'description': custom_input.description,
            'issuetype': {
                'name': issue_type
            }
    }

    jiraOptions = {'server': jira_url}  # Change this to refer to your Jira URL
    try:
        jira = JIRA(options=jiraOptions, basic_auth=(email,api_token))
        print(f"issue_data : {issue_data}")
        response =jira.create_issue(fields=issue_data)
        print(f"Jira Output:- {response.key}")
        result_payload = {
            "jira_d": response.key,
            "description": custom_input.description,
            "priority": custom_input.priority,
            "summary": custom_input.summary
        }
        result_payload = json.dumps(result_payload)
    except Exception as e:
        print(f"Failed to create jira ticket: {e}")
    print(f"JSON Output:- {result_payload}")
    return result_payload



@tool
def create_status_page_tool(custom_input: MyCustomJiraToolInput):
    """
    Create a new status page. From the Incident map below variables from the input:
        jira_id = jira_id
        priority = priority
        summary =summary
        description=description
        segment=segment
        product=product
    """
    try:
        # Example of creating an Incident object
        incident_data = {
            "incident": {
                "name": f"{custom_input.jira_id} - {custom_input.priority} - {custom_input.summary}",
                "status": "investigating",
                "impact_override": "none",
                "scheduled_remind_prior": False,
                "auto_transition_to_maintenance_state": False,
                "auto_transition_to_operational_state": False,
                "scheduled_auto_in_progress": False,
                "scheduled_auto_completed": False,
                "auto_transition_deliver_notifications_at_start": False,
                "auto_transition_deliver_notifications_at_end": False,
                "metadata": {},
                "deliver_notifications": False,
                "auto_tweet_at_beginning": False,
                "auto_tweet_on_completion": False,
                "auto_tweet_on_creation": False,
                "auto_tweet_one_hour_before": False,
                "backfill_date": "string",
                "backfilled": False,
                "body": f"{custom_input.jira_id} - {custom_input.priority} - {custom_input.description}",
                "scheduled_auto_transition": True
            }
        }
        url = f"{status_page_url}/pages/cgdn7cbyygwm/incidents"
        replacements_dict = {"ICD_NUMER": f"{custom_input.jira_id}", "ISSUE_DESCRIPTION": f"{custom_input.summary}",
                             "IMPACTED_SEGMENT": f"{custom_input.segment}", "IM_IMPACTED_SERVICE": f"{custom_input.product}"}

        # Original document ID

        original_document_id = os.getenv("WHITEBOARD_TEMPLATE_DOC_ID")
        document_name=f"{custom_input.jira_id} - {custom_input.summary}"
        # Call the function
        new_document_id,document_link = fetch_clone_and_replace(original_document_id, replacements_dict,document_name)
        print(f"WhiteBoard Created with id : - {new_document_id} and link - {document_link}")
        print(f"request : - {incident_data}")


        try:
            response = requests.post(url, json=incident_data, headers=status_page_headers)
            response.raise_for_status()  # Raise an error for HTTP errors
            print(f"Response - {response.json()}")
            print("\n\n$$$$$$$$$$$$$$$$$$$$$$$$$")
            result_payload = {
                "jira_d": custom_input.jira_id,
                "description": custom_input.description,
                "priority": custom_input.priority,
                "status_io_id": response.json()["id"],
                "summary": custom_input.summary,
                "white_board_id": new_document_id,
                "white_board_link": document_link,
            }
            result_payload = json.dumps(result_payload)
            print(f"******* status page result_payload *******:- {result_payload}")
            return result_payload
        except requests.exceptions.RequestException as e:
            print(f"Failed to create status page: {e}")
            raise
        except Exception as e:
            print(f"Failed to create Status Page: {e}")
            raise
    except Exception as e:
        print(f"Error in create_status_page_tool: {e}")
        raise

@tool
def my_custom_tool():
    """This is custom tool to read and process the file with no input."""
    try:
        to = os.getenv("MERCHANT_INSENSITIVE_TO_EMAIL")
        email_template = open("EmailTemplate.html", "r").read()

        email_template_json = json.loads(email_template)
        subject = email_template_json["subject"]
        body = str(email_template_json["body"]).replace("\\", "")

        if "issuing" in body.lower():
            to = os.getenv("ISSUING_INSENSITIVE_TO_EMAIL")

        send_email(to, email, subject, body)
        send_gmeet_invite(to, email, subject, body)

        return f"email and google meet invitation sent successfully to {to}"
    except Exception as e:
        print(f"Failed to create ticket: {e}")

@tool
def my_custom_tool_no_data():
    """This is custom tool to read and process the file with no input."""
    try:
        to = os.getenv("MERCHANT_SENSITIVE_TO_EMAIL")

        email_template_no_data = open("EmailTemplateNoData.html", "r").read()

        email_template_json = json.loads(email_template_no_data)
        subject = email_template_json["subject"]
        body = str(email_template_json["body"]).replace("\\", "")

        if "issuing" in body.lower():
            to = os.getenv("ISSUING_SENSITIVE_TO_EMAIL")

        send_email(to, email, subject, body)

        return f"email sent successfully to {to}"
    except Exception as e:
        print(f"Failed to create ticket: {e}")

def send_email(email_to, email_from, email_subject, email_body):
    try:
        # Authenticate and get credentials
        # flow = InstalledAppFlow.from_client_secrets_file("credentials.json", ["https://www.googleapis.com/auth/gmail.send"])
        # creds = flow.run_local_server(port=0)
        creds = None
        if os.path.exists("gmail_token.json"):
            creds = Credentials.from_authorized_user_file("gmail_token.json",
                                                          ["https://www.googleapis.com/auth/gmail.send"])
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", ["https://www.googleapis.com/auth/gmail.send"])
                creds = flow.run_local_server(port=0)
            with open('gmail_token.json', 'w') as token:
                token.write(creds.to_json())

        gmail_service = build("gmail", "v1", credentials=creds)

        # Create a MIMEText email message
        message = MIMEMultipart()
        message.attach(MIMEText(email_body, 'html'))
        # message = MIMEText(email_body)
        message['to'] = email_to
        message['from'] = email_from
        message['subject'] = email_subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()  # Encode the email

        # Send email
        result = gmail_service.users().messages().send(userId="me", body={"raw": raw_message}).execute()

        print(f"Email sent successfully! Message ID: {result['id']}")
    except Exception as e:
        print(f"Failed to create ticket: {e}")


def send_gmeet_invite(email_to, email_from, email_subject, email_body):
    try:
        timezone = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(timezone)
        future_time = current_time + timedelta(hours=2)
        formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        start = f"{formatted_time[:-2]}:{formatted_time[-2:]}"
        formatted_time = future_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        end = f"{formatted_time[:-2]}:{formatted_time[-2:]}"

        creds = None
        if os.path.exists("calendar_token.json"):
            creds = Credentials.from_authorized_user_file("calendar_token.json",
                                                          ["https://www.googleapis.com/auth/gmail.send"])
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", ["https://www.googleapis.com/auth/gmail.send"])
                creds = flow.run_local_server(port=0)
            with open('calendar_token.json', 'w') as token:
                token.write(creds.to_json())

        calendar_service = build('calendar', 'v3', credentials=creds)

        attendees = [{"email": emailId} for emailId in email_to.split(";")]

        event = {
            "summary": email_subject,
            "location": "Virtual",
            "description": email_body,
            "start": {
                "dateTime": start,  # Start time in ISO 8601
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": end,  # End time in ISO 8601
                "timeZone": "Asia/Kolkata",
            },
            "attendees": attendees,
            "conferenceData": {
                "createRequest": {
                    "requestId": "randomString123",
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                },
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        # Create the event
        event_calendar = calendar_service.events().insert(
            calendarId="primary",
            body=event,
            conferenceDataVersion=1
        ).execute()


        print(f"Event created: {event_calendar.get('htmlLink')}")
    except Exception as e:
        print(f"Failed to create ticket: {e}")

custom_email_template_tool = FileReadTool(file_path="email_template_sample.html")

SCOPES = ["https://www.googleapis.com/auth/documents.readonly","https://www.googleapis.com/auth/documents",'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_JSON =os.getenv("SERVICE_ACCOUNT_JSON")
def authenticate_google_api():
    """Authenticate and return Google API credentials."""
    return ServiceCredential.from_service_account_file(SERVICE_ACCOUNT_JSON, scopes=SCOPES)


def clone_google_doc(source_doc_id,document_name):
    """
    Clone a Google Document, including all text, styles, images, and other elements.

    :param document_name:
    :param source_doc_id: The ID of the source document to clone.
    :return: The ID of the cloned document.
    """
    # Authenticate using the service account
    credentials = authenticate_google_api()

    # Build the Google Drive service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Step 1: Copy the source document
    copy_metadata = {'name': document_name}
    copied_file = drive_service.files().copy(fileId=source_doc_id, body=copy_metadata).execute()
    cloned_doc_id = copied_file.get('id')
    # Grant edit permissions to all users
    permissions = {
        'role': 'writer',
        'type': 'anyone'
    }
    drive_service.permissions().create(fileId=cloned_doc_id, body=permissions).execute()
    # Get the web content link of the newly created file
    file = drive_service.files().get(fileId=cloned_doc_id, fields='webContentLink').execute()
    # Prioritize webContentLink if available
    if 'webContentLink' in file:
        file_link = file['webContentLink']
    else:
        # Construct the link manually using alternateLink
        file_link = f"https://drive.google.com/file/d/{cloned_doc_id}/view?usp=sharing"

    return cloned_doc_id,file_link

def fetch_clone_and_replace(original_document_id, replacements,document_name):
    """
    Fetch an existing Google Doc, clone it to a new document,
    and replace specific strings based on a dictionary of replacements.
    :param document_name: The name of the document.
    :param original_document_id: The ID of the original document to fetch.
    :param replacements: A dictionary where keys are search strings and values are replacements.
    """
    credentials = authenticate_google_api()
    docs_service = build('docs', 'v1', credentials=credentials)

    # Step 1: Fetch the content of the existing document
    new_doc_id, document_link=clone_google_doc(original_document_id,document_name)
    #Step 4: Replace each text based on the replacements dictionary
    replace_requests = []
    for search_text, replace_text in replacements.items():
        replace_requests.append({
            'replaceAllText': {
                'containsText': {
                    'text': search_text,
                    'matchCase': True,
                },
                'replaceText': replace_text,
            }
        })

    if replace_requests:
        docs_service.documents().batchUpdate(
            documentId=new_doc_id,
            body={'requests': replace_requests}
        ).execute()
        print(f"Replacements completed in the new document.")

    return new_doc_id,document_link