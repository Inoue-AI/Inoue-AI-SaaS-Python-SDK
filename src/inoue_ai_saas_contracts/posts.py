from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class PostMedia(BaseModel):
    id: str
    post_id: str
    asset_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class PostTargetRecord(BaseModel):
    id: str
    post_id: str
    platform: str
    connected_account_id: str | None = None
    status: str
    remote_post_id: str | None = None
    error_json: dict[str, Any] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
