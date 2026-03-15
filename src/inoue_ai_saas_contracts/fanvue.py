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


class FanvueConnectedAccount(ConnectedAccount):
    pass


class FanvueConversation(BaseModel):
    id: str
    connected_account_id: str
    model_id: str
    remote_conversation_id: str
    title: str | None = None
    participant: dict | None = None
    last_message: str | None = None
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_message_at: datetime | None = None
    status: str | None = None
    unread_count: int | None = None
    lock: ConversationLock | None = None
    requests: list[ConversationLockRequest] | None = None


class FanvueMessage(BaseModel):
    id: str
    conversation_id: str
    body_text: str
    direction: str
    sent_at: datetime | None = None
    sent_by_user_id: str | None = None
    operator_name: str | None = None
    attachments: list[dict] | None = None
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class FanvueCreator(BaseModel):
    id: str
    handle: str | None = None
    display_name: str | None = None
    email: str | None = None
    avatar_url: str | None = None
    status: str | None = None
    country: str | None = None


class ConversationLock(BaseModel):
    conversation_id: str
    locked_by_user_id: str | None = None
    locked_by_user_email: str | None = None
    lock_status: str
    locked_at: datetime | None = None
    last_activity_at: datetime | None = None
    updated_at: datetime | None = None


class ConversationLockRequest(BaseModel):
    id: str
    conversation_id: str
    requested_by_user_id: str
    requested_by_user_email: str | None = None
    status: str
    resolved_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ModelPlatformIdentity(BaseModel):
    id: str | None = None
    model_id: str
    connected_account_id: str
    remote_identity_id: str
    remote_creator_id: str | None = None
    remote_creator_data: dict | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class FanvueConnectStart(BaseModel):
    url: str
    state: str
    mode: str


class FanvueTokenRefresh(BaseModel):
    connected_account_id: str
    access_token: str
    refresh_token: str
    token_expires_at: datetime


class ModelIdentityMapRequest(BaseModel):
    model_id: str
    connected_account_id: str = Field(validation_alias=AliasChoices("connected_account_id", "account_id"))
    remote_identity_id: str | None = None
    remote_creator_id: str | None = None
    remote_creator_data: dict | None = None
