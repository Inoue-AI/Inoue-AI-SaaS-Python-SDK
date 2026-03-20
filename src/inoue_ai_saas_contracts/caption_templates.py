"""Contracts for built-in caption templates and user custom caption templates."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

# ── Built-in Caption Template ──


class CaptionTemplateResponse(BaseModel):
    id: str
    name: str
    slug: str
    config_style: dict[str, Any] = Field(default_factory=dict)
    highlight_style: dict[str, Any] = Field(default_factory=dict)
    subs: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    is_builtin: bool = True
    is_premium: bool = False
    sort_order: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CaptionTemplateListQuery(BaseModel):
    tag: str | None = None
    is_premium: bool | None = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


# ── User Custom Caption Template ──


class UserCaptionTemplateResponse(BaseModel):
    id: str
    owner_user_id: str
    owner_org_id: str | None = None
    name: str
    slug: str
    base_template_id: str | None = None
    config_style: dict[str, Any] = Field(default_factory=dict)
    highlight_style: dict[str, Any] = Field(default_factory=dict)
    subs: dict[str, Any] = Field(default_factory=dict)
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserCaptionTemplateCreateRequest(BaseModel):
    name: str
    slug: str
    base_template_id: str | None = None
    owner_org_id: str | None = None
    config_style: dict[str, Any] = Field(default_factory=dict)
    highlight_style: dict[str, Any] = Field(default_factory=dict)
    subs: dict[str, Any] = Field(default_factory=dict)


class UserCaptionTemplateUpdateRequest(BaseModel):
    name: str | None = None
    config_style: dict[str, Any] | None = None
    highlight_style: dict[str, Any] | None = None
    subs: dict[str, Any] | None = None


class UserCaptionTemplateListQuery(BaseModel):
    owner_org_id: str | None = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
