from dataclasses import field

from pydantic import BaseModel, Field


class PriorityModel(BaseModel):
    priority: str
    description: str
    summary: str

class JiraModel(BaseModel):
    jira_id: str = Field(default = "")
    description: str = Field(default = "")
    priority: str = Field(default = "")
    summary: str = Field(default="")
    # my_list: list = field(default_factory=list)

class EmailTemplate(BaseModel):
    subject: str
    # to: list
    body: str
    summary: str
    jira_id: str