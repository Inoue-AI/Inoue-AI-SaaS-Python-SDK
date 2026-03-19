"""Referral program contracts."""

from __future__ import annotations

import datetime as dt
from typing import Literal

from pydantic import BaseModel


class ReferralSummaryResult(BaseModel):
    users_per_reward: int
    credits_per_reward: int
    max_codes_per_user: int
    referred_users_count: int
    earned_credits_total: int
    rewards_earned_count: int
    active_codes_count: int
    pending_users_count: int
    next_reward_users_remaining: int


class ReferralCodeCreateRequest(BaseModel):
    pass


class ReferralCodeRevokeRequest(BaseModel):
    pass


class ReferralCodeResponse(BaseModel):
    id: str
    code: str
    code_hint: str
    uses_count: int
    status: Literal["active", "revoked"]
    is_revoked: bool = False
    created_at: dt.datetime | None = None
    revoked_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
