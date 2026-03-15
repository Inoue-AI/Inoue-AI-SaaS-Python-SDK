from __future__ import annotations

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationQuery(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class DateRangeQuery(BaseModel):
    start: datetime | None = None
    end: datetime | None = None


class OrgListQuery(PaginationQuery):
    search: str | None = None
    owner_id: str | None = None
    q: str | None = None


class OrgMemberListQuery(PaginationQuery):
    role: str | None = None
    status: str | None = None
    q: str | None = None


class ModelListQuery(PaginationQuery, DateRangeQuery):
    owner_type: str | None = None
    owner_id: str | None = None
    shared_with_me: bool | None = None
    org_id: str | None = None
    name: str | None = None
    q: str | None = None


class PromptTemplateListQuery(PaginationQuery, DateRangeQuery):
    owner_type: str | None = None
    owner_id: str | None = None
    org_id: str | None = None
    model_id: str | None = None
    tag: str | None = None
    locked: bool | None = None
    search: str | None = None
    q: str | None = None


class PromptRunListQuery(PaginationQuery, DateRangeQuery):
    org_id: str | None = None
    model_id: str | None = None
    template_id: str | None = None
    status: str | None = None
    q: str | None = None


class JobListQuery(PaginationQuery, DateRangeQuery):
    org_id: str | None = None
    model_id: str | None = None
    pipeline_id: str | None = None
    type: str | None = None
    status: str | None = None
    engine_type: str | None = None
    q: str | None = None


class AssetListQuery(PaginationQuery, DateRangeQuery):
    owner_type: str | None = None
    owner_id: str | None = None
    org_id: str | None = None
    model_id: str | None = None
    run_id: str | None = None
    type: str | None = None
    archived: bool | None = None
    q: str | None = None


class CollectionListQuery(PaginationQuery):
    owner_type: str | None = None
    owner_id: str | None = None
    org_id: str | None = None
    model_id: str | None = None
    search: str | None = None
    q: str | None = None


class AlbumListQuery(PaginationQuery):
    owner_type: str | None = None
    owner_id: str | None = None
    org_id: str | None = None
    model_id: str | None = None
    search: str | None = None
    q: str | None = None


class PostListQuery(PaginationQuery, DateRangeQuery):
    model_id: str | None = None
    status: str | None = None
    platform: str | None = None
    q: str | None = None


class ScheduleListQuery(PaginationQuery, DateRangeQuery):
    calendar: str | None = None
    model_id: str | None = None
    platform_id: str | None = None
    content_type_id: str | None = None
    status: str | None = None
    q: str | None = None


class RevenueEventListQuery(PaginationQuery, DateRangeQuery):
    model_id: str | None = None
    org_id: str | None = None
    q: str | None = None


class NotificationListQuery(PaginationQuery, DateRangeQuery):
    model_id: str | None = None
    unread_only: bool | None = None
    q: str | None = None


class WebhookEventListQuery(PaginationQuery, DateRangeQuery):
    event_type: str | None = None
    status: str | None = None
    q: str | None = None


class UsageListQuery(PaginationQuery, DateRangeQuery):
    model_id: str | None = None
    job_type: str | None = None
    q: str | None = None


class PoolingInviteListQuery(PaginationQuery):
    status: str | None = None


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
