from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel

from .enums import JobType


class UserWallet(BaseModel):
    user_id: str
    balance_credits: Decimal
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UsageRecord(BaseModel):
    id: str
    user_id: str
    model_id: str | None = None
    job_id: str | None = None
    job_type: JobType | str
    compute_seconds: int | None = None
    cost_credits: Decimal
    created_at: datetime | None = None


class RateCardEntry(BaseModel):
    id: str | None = None
    job_type: JobType | str
    job_title: str | None = None
    engine_type: str | None = None
    cost_credits: Decimal
    rate_unit: str = "credits"
    params: dict[str, Any] | None = None
