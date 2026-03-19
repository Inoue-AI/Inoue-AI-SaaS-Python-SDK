"""Application catalog contracts."""

from __future__ import annotations

import datetime as dt

from pydantic import BaseModel, Field

from .pagination import PaginationQuery


class AppListQuery(PaginationQuery):
    q: str | None = None
    include_inactive: bool | None = False


class AppVersionListQuery(PaginationQuery):
    published_only: bool | None = True


class AppAccessResponse(BaseModel):
    allowed: bool
    reason: str | None = None


class AppLatestVersionResponse(BaseModel):
    version: str
    required: bool = False
    notes: str | None = None
    downloads: dict[str, str] = Field(default_factory=dict)


class AppVersionPublicResponse(BaseModel):
    id: str
    version: str
    required: bool = False
    notes: str | None = None
    is_published: bool = True
    released_at: dt.datetime | None = None
    downloads: dict[str, str] = Field(default_factory=dict)


class AppCatalogItemResponse(BaseModel):
    id: str
    slug: str
    name: str
    description: str | None = None
    icon_url: str | None = None
    latest_version: str | None = None
    required: bool | None = None
    notes: str | None = None
    downloads: dict[str, str] = Field(default_factory=dict)
