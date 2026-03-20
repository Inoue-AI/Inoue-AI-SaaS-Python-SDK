"""Push notification subscription contracts."""

from __future__ import annotations

from pydantic import BaseModel


class PushSubscriptionKeys(BaseModel):
    p256dh: str
    auth: str


class PushSubscriptionCreateRequest(BaseModel):
    endpoint: str
    keys: PushSubscriptionKeys
    org_id: str | None = None


class PushSubscriptionResponse(BaseModel):
    id: str
    user_id: str
    org_id: str | None = None
    endpoint: str
    created_at: str
    updated_at: str


class VapidPublicKeyResponse(BaseModel):
    public_key: str
