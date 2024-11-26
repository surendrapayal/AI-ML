from pydantic import BaseModel

class PriorityModel(BaseModel):
    priority: str
    description: str

class JiraModel(BaseModel):
    jiraId: int
    jiraDescription: str