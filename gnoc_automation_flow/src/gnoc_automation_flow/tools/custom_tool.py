
from crewai_tools import tool
from pydantic import BaseModel, Field
import requests
# from gnoc_automation_flow.src.gnoc_automation_flow.types import JiraModel
from dotenv import load_dotenv
from jira import JIRA
from crewai_tools import tool
from ..model.status_page import Incident
from sympy import print_mathml
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
import base64
import pytz
from ..types import JiraModel

# loading variables from .env file
load_dotenv()
# Jira credentials and endpoint
jira_url = 'https://rahuluraneai.atlassian.net/'
api_token = os.getenv("JIRA_API_TOKEN")  # You can generate this from your Atlassian account
email = 'rahulurane.ai@gmail.com'  # Your Jira login email
project_key = 'Gnoc-Issue-tracker'  # Replace with your Jira project key
issue_type = 'Bug'  # Issue type (Bug in this case)
status_page_url = "https://api.statuspage.io/v1"
status_page_headers = {
    "Authorization": f"OAuth {os.getenv("STATUS_API_TOKEN")}",
    "Content-Type": "application/json"
}

class MyCustomJiraToolInput(BaseModel):
    """Input schema for MyCustomJiraTool"""
    priority: str = Field(..., description="Priority of the issue.")
    description: str = Field(..., description="Description of the issue.")
    jira_id: str = Field("JIRA-123", description="")
    summary: str = Field("", description="")



@tool
def my_custom_jira_tool_new(custom_input: MyCustomJiraToolInput):
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
    """
    print("$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")
    print(custom_input)
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
                "status_io_id": custom_input.priority,
                "summary": custom_input.summary
            }
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to create status page: {e}")
            raise
        except Exception as e:
            print(f"Failed to create Status Page: {e}")
            raise
    except Exception as e:
        print(f"Error in create_status_page_tool: {e}")
        raise

class MyCustomGoogleInput(BaseModel):
    """Input schema for MyCustomJiraTool"""
    subject: str = Field("", description="email subject.")
    # to: list = Field(..., description="email to.")
    body: str = Field("", description="email body.")


@tool
def my_custom_email_calendar_tool(custom_input: MyCustomGoogleInput):
    """This tool is used to draft an email and calendar invite."""
    try:
        to = os.getenv("TO_EMAIL")
        print(f"email subject inside email tool:- {custom_input.subject}")
        print(f"email to inside email tool:- {to}")
        print(f"email body inside email tool:- {custom_input.body}")

        # Authenticate and get credentials
        # flow = InstalledAppFlow.from_client_secrets_file("credentials.json", ["https://www.googleapis.com/auth/gmail.send"])
        # creds = flow.run_local_server(port=0)
        creds = None
        if os.path.exists("gmail_token.json"):
            creds = Credentials.from_authorized_user_file("gmail_token.json", ["https://www.googleapis.com/auth/gmail.send"])
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
        message = MIMEText(custom_input.body)
        # message['to'] = "; ".join(custom_input.to)
        message['to'] = to
        # message['to'] = custom_input.to
        # message['from'] = "rahulurane.ai@gmail.com"
        message['from'] = email
        message['subject'] = custom_input.subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()  # Encode the email

        # Send email
        result = gmail_service.users().messages().send(userId="me", body={"raw": raw_message}).execute()

        print(f"Email sent successfully! Message ID: {result['id']}")


        timezone = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(timezone)
        future_time = current_time + timedelta(hours=2)
        formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        start = f"{formatted_time[:-2]}:{formatted_time[-2:]}"
        formatted_time = future_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        end = f"{formatted_time[:-2]}:{formatted_time[-2:]}"

        creds = None
        if os.path.exists("calendar_token.json"):
            creds = Credentials.from_authorized_user_file("calendar_token.json", ["https://www.googleapis.com/auth/gmail.send"])
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

        event = {
            "summary": custom_input.subject,
            "location": "Virtual",
            "description": custom_input.body,
            "start": {
                "dateTime": start,  # Start time in ISO 8601
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": end,  # End time in ISO 8601
                "timeZone": "Asia/Kolkata",
            },
            "attendees": [
                # {"email": custom_input.to.split(";")[0].strip()},
                # {"email": custom_input.to.split(";")[1].strip()},
                # {"email": custom_input.to.split(";")[2].strip()},
                # {"email": custom_input.to[0].strip()},
                # {"email": custom_input.to[1].strip()},
                # {"email": custom_input.to[2].strip()},
                {"email": os.getenv("TO_EMAIL").split(";")[0].strip()},
                {"email": os.getenv("TO_EMAIL").split(";")[1].strip()},
                {"email": os.getenv("TO_EMAIL").split(";")[2].strip()},
            ],
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
        return "email and google meet invitation sent successfully"
    except Exception as e:
        print(f"Failed to create ticket: {e}")