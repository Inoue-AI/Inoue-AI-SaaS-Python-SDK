"""Contracts for the private content feature."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

# ── Fixed costs ──────────────────────────────────────────────────────────────

MOTIONMUSE_CREDIT_COST = Decimal("5")


# ── Response models ──────────────────────────────────────────────────────────


class PrivateContentProviderResponse(BaseModel):
    id: str
    slug: str
    name: str
    description: str | None = None
    api_base_url: str
    is_active: bool
    icon_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PrivateContentUserAccessResponse(BaseModel):
    id: str
    user_id: str
    granted_by_user_id: str
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    revoked_at: datetime | None = None


class PrivateContentTemplateResponse(BaseModel):
    id: str
    provider_id: str
    external_id: str
    code: str | None = None
    title: str
    description: str | None = None
    version: str | None = None
    sensitive: bool = False
    free_trial: bool = False
    newly_added: bool = False
    author: str | None = None
    tags: list[str] = Field(default_factory=list)
    score: float | None = None
    image_url: str | None = None
    image_width: int | None = None
    image_height: int | None = None
    video_url: str | None = None
    video_width: int | None = None
    video_height: int | None = None
    preview_url: str | None = None
    preview_width: int | None = None
    preview_height: int | None = None
    last_synced_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PrivateContentCollectionResponse(BaseModel):
    id: str
    provider_id: str
    external_id: str
    name: str | None = None
    version: str | None = None
    status: str
    template_external_id: str | None = None
    template_title: str | None = None
    image_url: str | None = None
    image_width: int | None = None
    image_height: int | None = None
    video_url: str | None = None
    video_width: int | None = None
    video_height: int | None = None
    favorited: bool = False
    payload: dict | None = None
    last_synced_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


# ── Insert payloads ──────────────────────────────────────────────────────────


class PrivateContentProviderInsert(BaseModel):
    slug: str
    name: str
    description: str | None = None
    api_base_url: str
    is_active: bool = True
    icon_url: str | None = None


class PrivateContentUserAccessInsert(BaseModel):
    user_id: str
    granted_by_user_id: str
    is_active: bool = True


class PrivateContentUserAccessUpdate(BaseModel):
    is_active: bool | None = None
    revoked_at: datetime | None = None


class PrivateContentTemplateUpsert(BaseModel):
    provider_id: str
    external_id: str
    code: str | None = None
    title: str
    description: str | None = None
    version: str | None = None
    sensitive: bool = False
    free_trial: bool = False
    newly_added: bool = False
    author: str | None = None
    tags: list[str] = Field(default_factory=list)
    score: float | None = None
    image_url: str | None = None
    image_width: int | None = None
    image_height: int | None = None
    video_url: str | None = None
    video_width: int | None = None
    video_height: int | None = None
    preview_url: str | None = None
    preview_width: int | None = None
    preview_height: int | None = None
    last_synced_at: datetime | None = None
    raw_json: dict | None = None


class PrivateContentCollectionUpsert(BaseModel):
    provider_id: str
    external_id: str
    name: str | None = None
    version: str | None = None
    status: str = "completed"
    template_external_id: str | None = None
    template_title: str | None = None
    image_url: str | None = None
    image_width: int | None = None
    image_height: int | None = None
    video_url: str | None = None
    video_width: int | None = None
    video_height: int | None = None
    favorited: bool = False
    payload: dict | None = None
    last_synced_at: datetime | None = None
    raw_json: dict | None = None


# ── Request models ───────────────────────────────────────────────────────────


class PrivateContentGenerateRequest(BaseModel):
    template_id: str
    source_asset_id: str | None = None
    source_video_asset_id: str | None = None
    is_extension: bool = False
    audio: bool = False
    prompt: str | None = None


class PrivateContentProviderUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    api_base_url: str | None = None
    is_active: bool | None = None
    icon_url: str | None = None


# ── Query models ─────────────────────────────────────────────────────────────


class PrivateContentTemplateListQuery(BaseModel):
    page: int = 1
    page_size: int = 20
    provider_slug: str | None = None
    search: str | None = None
    sensitive: bool | None = None
    order: str | None = None


class PrivateContentCollectionListQuery(BaseModel):
    page: int = 1
    page_size: int = 20
    provider_slug: str | None = None
    status: str | None = None
