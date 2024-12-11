from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class PriorityModel(BaseModel):
    """Priority model class"""
    description: str = Field(..., description="default description")
    summary: str = Field(..., description="default summary")
    segment: str = Field(..., description="default segment")
    product: str = Field(..., description="default product")
    priority: str = Field(..., description="default priority")
    impact: str = Field(..., description="default impact")
    urgency: str = Field(..., description="default urgency")

class MyCustomJiraToolInput(BaseModel):
    """Input schema for MyCustomJiraTool"""
    priority: str = Field(..., description="Priority of the issue.")
    description: str = Field(..., description="Description of the issue.")
    jira_id: str = Field("JIRA-123", description="")
    summary: str = Field("DUMMY SUMMARY", description="")

class JiraModel(BaseModel):
    """Jira model class"""
    jira_id: str = Field(default = "")
    description: str = Field(default = "")
    priority: str = Field(default = "")
    summary: str = Field(default="")
    status_io_id: str = Field(default="")

class EmailTemplate(BaseModel):
    subject: str
    body: str

class Incident(BaseModel):
    name: str
    status: str
    impact_override: str
    scheduled_remind_prior: bool
    auto_transition_to_maintenance_state: bool
    auto_transition_to_operational_state: bool
    scheduled_auto_in_progress: bool
    scheduled_auto_completed: bool
    auto_transition_deliver_notifications_at_start: bool
    auto_transition_deliver_notifications_at_end: bool
    metadata: Dict[str, Any]
    deliver_notifications: bool
    auto_tweet_at_beginning: bool
    auto_tweet_on_completion: bool
    auto_tweet_on_creation: bool
    auto_tweet_one_hour_before: bool
    backfill_date: str
    backfilled: bool
    body: str
    scheduled_auto_transition: bool


class Model(BaseModel):
    incident: Optional[Incident] = None