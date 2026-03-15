from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

DISCORD_WEBHOOK_EVENT_TYPES = [
    "job.completed",
    "asset.created",
    "prompt_template.created",
    "prompt_version.created",
    "model.shared",
    "member.joined",
    "album.asset_added",
    "collection.created",
    "schedule.item_created",
]


class OrgDiscordWebhookCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    webhook_url: str = Field(min_length=1, max_length=2048)
    is_enabled: bool = True
    event_types: list[str] = Field(default_factory=list)


class OrgDiscordWebhookUpdateRequest(BaseModel):
    name: str | None = None
    webhook_url: str | None = None
    is_enabled: bool | None = None
    event_types: list[str] | None = None


class OrgDiscordWebhookResponse(BaseModel):
    id: str
    org_id: str
    name: str
    webhook_url: str
    is_enabled: bool
    created_by_user_id: str | None = None
    event_types: list[str] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OrgDiscordWebhookTestRequest(BaseModel):
    pass


class OrgDiscordWebhookTestResponse(BaseModel):
    success: bool
    message: str
