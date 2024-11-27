from crewai_tools import tool
from pydantic import BaseModel, Field
# from gnoc_automation_flow.src.gnoc_automation_flow.types import JiraModel


class MyCustomJiraToolInput(BaseModel):
    """Input schema for MyCustomJiraTool"""
    priority: str = Field(..., description="Priority of the issue.")
    description: str = Field(..., description="Description of the issue.")



@tool
def my_custom_jira_tool_new(custom_input: MyCustomJiraToolInput) -> dict[str, int | str]:
    """A custom tool that processes multiple inputs."""
    print(f"priority inside jira tool:- {custom_input.priority}")
    print(f"description inside jira tool:- {custom_input.description}")
    result_payload = {
        "jiraId": 123456,
        "jiraDescription": custom_input.description
    }
    print(f"JSON Output:- {result_payload}")
    return result_payload