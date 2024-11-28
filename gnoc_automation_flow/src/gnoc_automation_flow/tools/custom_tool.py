
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



@tool
def my_custom_jira_tool_new(custom_input: MyCustomJiraToolInput):
    """
        Create a Jira ticket with the given details.
        if this method is executed then stop
    """
    print(f"priority inside jira tool:- {custom_input.priority}")
    print(f"description inside jira tool:- {custom_input.description}")
    # Create the Jira issue payload (JSON body)
    issue_data = {
         'project': {
             'id': '10000'
            },
            'summary': f'Bug summary example {custom_input.priority}',
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
            "priority": custom_input.priority
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
    """
    print("$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")
    print(custom_input)
    try:
        # Example of creating an Incident object
        incident_data = {
            "incident": {
                "name": f"{custom_input.jira_id} - {custom_input.priority}",
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
                "status_io_id": custom_input.priority
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
