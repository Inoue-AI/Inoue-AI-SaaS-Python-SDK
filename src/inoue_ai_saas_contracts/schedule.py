from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SchedulePlatform(BaseModel):
    id: str
    key: str
    label: str
    logo_key: str | None = None
    sort_order: int | None = None
    is_active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ScheduleContentType(BaseModel):
    id: str
    platform_id: str
    key: str
    label: str
    sort_order: int | None = None
    is_active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ScheduleCatalogPlatform(SchedulePlatform):
    content_types: list[ScheduleContentType] = Field(default_factory=list)


class ScheduleCatalogResponse(BaseModel):
    platforms: list[ScheduleCatalogPlatform] = Field(default_factory=list)
    statuses: list[str] = Field(default_factory=list)


class ScheduleEntryCreateRequest(BaseModel):
    org_id: str | None = None
    model_id: str
    platform_id: str
    content_type_id: str
    scheduled_for: datetime
    asset_ids: list[str] = Field(default_factory=list)
    notes: str | None = None


class ScheduleEntryUpdateRequest(BaseModel):
    org_id: str | None = None
    model_id: str | None = None
    platform_id: str | None = None
    content_type_id: str | None = None
    scheduled_for: datetime | None = None
    asset_ids: list[str] | None = None
    notes: str | None = None


class ScheduleEntryResponse(BaseModel):
    id: str
    owner_type: str | None = None
    owner_user_id: str | None = None
    owner_org_id: str | None = None
    model_id: str | None = None
    model_name: str | None = None
    platform_id: str | None = None
    platform_key: str | None = None
    platform_label: str | None = None
    content_type_id: str | None = None
    content_type_key: str | None = None
    content_type_label: str | None = None
    scheduled_for: datetime
    status: str
    asset_ids: list[str] = Field(default_factory=list)
    notes: str | None = None
    created_by_user_id: str | None = None
    completed_by_user_id: str | None = None
    completed_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ScheduleCompleteRequest(BaseModel):
    schedule_id: str
    completed_at: datetime | None = None


class ScheduleDeleteRequest(BaseModel):
    schedule_id: str


# ── Recurring Rules ──


class RecurrenceSchema(BaseModel):
    """Custom recurrence definition. Extensible for future frequency types."""

    frequency: str  # daily, weekly, monthly
    interval: int = Field(default=1, ge=1, description="Every Nth frequency unit (e.g. every 2 weeks)")
    days_of_week: list[int] | None = Field(default=None, description="0=Mon..6=Sun (for weekly)")
    day_of_month: int | None = Field(default=None, ge=1, le=31, description="Day of month (for monthly)")
    time: str = Field(description="HH:MM in 24h format")
    timezone: str = Field(default="UTC", description="IANA timezone (e.g. Europe/Rome)")


class RecurringRuleCreateRequest(BaseModel):
    org_id: str | None = None
    event_type: str  # schedule_post, reminder
    label: str
    recurrence: RecurrenceSchema
    template: dict = Field(default_factory=dict, description="Event-specific payload template")


class RecurringRuleUpdateRequest(BaseModel):
    label: str | None = None
    recurrence: RecurrenceSchema | None = None
    template: dict | None = None
    is_active: bool | None = None


class RecurringRuleResponse(BaseModel):
    id: str
    owner_type: str | None = None
    owner_user_id: str | None = None
    owner_org_id: str | None = None
    event_type: str
    label: str
    recurrence: dict = Field(default_factory=dict)
    template: dict = Field(default_factory=dict)
    is_active: bool = True
    next_run_at: datetime | None = None
    last_run_at: datetime | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
