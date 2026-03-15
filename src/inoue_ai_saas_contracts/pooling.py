from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ModelPool(BaseModel):
    id: str
    model_id: str
    created_by_user_id: str | None = None
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ModelPoolMember(BaseModel):
    id: str
    pool_id: str
    user_id: str
    status: str
    weight_percent: int
    invited_at: datetime | None = None
    responded_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class PoolView(BaseModel):
    model_id: str
    pool: ModelPool | None = None
    members: list[ModelPoolMember] = []


class PoolingInvite(BaseModel):
    member_id: str
    pool_id: str
    model_id: str
    status: str
    weight_percent: int
    invited_at: datetime | None = None
    responded_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
