from typing import Type

from crewai.tools import BaseTool
from crewai_tools import tool
from pydantic import BaseModel, Field

from gnoc_automation_flow.types import JiraModel


class JiraTool:
    @tool
    def jira_tool(self, priority, description):
        # def jira_tool(priority: str, description: str):
        """Tool description for clarity."""
        # Tool logic here
        # print(f"priority inside jira tool:- {priority}")
        # print(f"description inside jira tool:- {description}")
        model = JiraModel()
        model.jiraId = 12345
        model.jiraDescription = "description"
        return model

#     def jira_tool(self, priority: str, description: str):
#         """Tool for Jira"""
#         print(f"priority inside jira tool:- {priority}")
#         print(f"description inside jira tool:- {description}")
#         model = JiraModel()
#         model.jiraId = 12345
#         model.jiraDescription = "description"
#         return model

# @tool
# def jira_tool():
#     # def jira_tool(priority: str, description: str):
#     """Tool description for clarity."""
#     # Tool logic here
#     # print(f"priority inside jira tool:- {priority}")
#     # print(f"description inside jira tool:- {description}")
#     model = JiraModel()
#     model.jiraId = 12345
#     model.jiraDescription = "description"
#     return model

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    argument: str = Field(..., description="Description of the argument.")


class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
