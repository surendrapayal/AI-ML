from dataclasses import field

from pydantic import BaseModel, Field


class PriorityModel(BaseModel):
    priority: str
    description: str

class JiraModel(BaseModel):
    jira_id: str = Field(default = "")
    description: str = Field(default = "")
    priority: str = Field(default = "")
    my_list: list = field(default_factory=list)