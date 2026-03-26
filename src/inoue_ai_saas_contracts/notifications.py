from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class InternalNotification(BaseModel):
    id: str
    org_id: str | None = None
    model_id: str | None = None
    title: str
    body: str
    target_user_id: str | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    deleted_at: datetime | None = None


class NotificationRead(BaseModel):
    id: str
    notification_id: str
    user_id: str
    read_at: datetime | None = None
    is_muted: bool | None = None
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NotificationItem(BaseModel):
    id: str
    org_id: str | None = None
    model_id: str | None = None
    title: str
    body: str
    created_at: datetime | None = None
    is_muted: bool = False
    read_at: datetime | None = None


class NotificationCounts(BaseModel):
    """Server-side aggregated notification counts (independent of pagination)."""

    total: int = 0
    unread: int = 0
    muted: int = 0


class NotificationModelMute(BaseModel):
    """A record of a user muting all notifications from a specific model."""

    id: str
    user_id: str
    model_id: str
    created_at: datetime | None = None
