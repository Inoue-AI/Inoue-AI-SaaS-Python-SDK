from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class RevenueEvent(BaseModel):
    id: str
    platform: str
    connected_account_id: str
    model_id: str | None = None
    remote_event_id: str
    revenue_type: str
    amount_cents: int
    currency: str
    occurred_at: datetime
    created_at: datetime | None = None


class RevenueSummary(BaseModel):
    total_cents: int
    events: list[RevenueEvent]
