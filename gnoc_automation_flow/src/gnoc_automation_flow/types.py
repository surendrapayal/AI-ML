from pydantic import BaseModel

class PriorityModel(BaseModel):
    priority: str
    description: str