from crewai_tools import tool
from pydantic import BaseModel, Field
# from gnoc_automation_flow.src.gnoc_automation_flow.types import JiraModel
from dotenv import load_dotenv
from jira import JIRA
from crewai_tools import tool
from sympy import print_mathml
import os
# loading variables from .env file
load_dotenv()
# Jira credentials and endpoint
jira_url = 'https://rahuluraneai.atlassian.net/'
api_token = os.getenv("JIRA_API_TOKEN")  # You can generate this from your Atlassian account
email = 'rahulurane.ai@gmail.com'  # Your Jira login email
project_key = 'Gnoc-Issue-tracker'  # Replace with your Jira project key
issue_type = 'Bug'  # Issue type (Bug in this case)

class MyCustomJiraToolInput(BaseModel):
    """Input schema for MyCustomJiraTool"""
    priority: str = Field(..., description="Priority of the issue.")
    description: str = Field(..., description="Description of the issue.")



@tool
def my_custom_jira_tool_new(custom_input: MyCustomJiraToolInput):
    """
        Create a Jira ticket with the given details.

        use issue-data as a request body for jira ticket creation
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
        print(f"Jira Output:- {response}")
        result_payload = {
            "jiraId": response,
            "jiraDescription": custom_input.description
        }
    except Exception as e:
        print(f"Failed to create ticket: {e}")
    print(f"JSON Output:- {result_payload}")
    return result_payload

