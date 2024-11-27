from dataclasses import field

from pydantic import BaseModel, Field


class PriorityModel(BaseModel):
    priority: str
    description: str

class JiraModel(BaseModel):
    jiraId: int = Field(default = 54321)
    jiraDescription: str = Field(default = "Temporary Description")
    my_list: list = field(default_factory=list)