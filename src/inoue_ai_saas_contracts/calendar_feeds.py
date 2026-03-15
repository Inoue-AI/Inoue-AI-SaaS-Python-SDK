from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class CalendarSubscriptionCreateRequest(BaseModel):
    label: str
    scope_type: str
    scope_org_id: str | None = None
    model_ids: list[str] | None = None
    timezone: str = "UTC"


class CalendarSubscriptionUpdateRequest(BaseModel):
    label: str | None = None
    model_ids: list[str] | None = None
    timezone: str | None = None
    is_active: bool | None = None


class CalendarSubscriptionResponse(BaseModel):
    id: str
    user_id: str
    label: str
    scope_type: str
    scope_org_id: str | None = None
    model_ids: list[str] | None = None
    timezone: str
    is_active: bool
    feed_url: str
    last_fetched_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
