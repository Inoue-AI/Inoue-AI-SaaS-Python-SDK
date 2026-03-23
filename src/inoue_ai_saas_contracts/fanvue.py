from __future__ import annotations

from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field


class ConnectedAccount(BaseModel):
    id: str
    platform: str
    owner_user_id: str | None = None
    owner_org_id: str | None = None
    label: str | None = None
    icon_url: str | None = None
    connected_by_user_id: str | None = None
    connected_by_email: str | None = None
    handle: str | None = None
    display_name: str | None = None
    model_ids: list[str] | None = None
    model_count: int | None = None
    model_identities: list[ModelPlatformIdentity] | None = None
    owner_org_name: str | None = None
    ownership: str | None = None  # "user" or "org"
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ModelPlatformIdentity(BaseModel):
    id: str | None = None
    model_id: str
    connected_account_id: str
    remote_identity_id: str
    remote_creator_id: str | None = None
    remote_creator_data: dict | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ModelIdentityMapRequest(BaseModel):
    model_id: str
    connected_account_id: str = Field(validation_alias=AliasChoices("connected_account_id", "account_id"))
    remote_identity_id: str | None = None
    remote_creator_id: str | None = None
    remote_creator_data: dict | None = None
