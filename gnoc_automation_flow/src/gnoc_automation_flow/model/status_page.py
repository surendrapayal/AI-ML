from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel


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