"""Lightweight Pydantic models for database row projections.

These models replace ``TypeAdapter(dict)`` usages throughout the codebase
when only a subset of columns is needed from a PostgREST query.  Each model
is named ``<Table>Row`` and contains only the fields that callers actually
access, keeping serialisation fast and explicit.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

# ── Generic operation results ───────────────────────────────────────────────


class GenericRow(BaseModel):
    """Fallback for delete/insert operations where only the ID matters."""

    id: str


class GenericInsertRow(BaseModel):
    """Insert response with id and created_at."""

    id: str
    created_at: datetime | None = None


# ── Users ───────────────────────────────────────────────────────────────────


class UserPreferencesRow(BaseModel):
    """Projection of users table for preferences-only queries."""

    preferences: dict[str, Any] | None = None


class UserEmailRow(BaseModel):
    """Projection of users table for email-only lookups."""

    id: str
    email: str | None = None


class UserPatchRow(BaseModel):
    """Result shape when patching user preferences."""

    id: str
    preferences: dict[str, Any] | None = None


# ── Private Content ─────────────────────────────────────────────────────────


class PrivateContentAccessRow(BaseModel):
    """Row from private_content_user_access for active-access checks."""

    user_id: str
    is_active: bool = False


class PrivateContentTemplateRow(BaseModel):
    """Row from private_content_templates for sync operations."""

    id: str
    external_id: str | None = None


class PrivateContentCollectionRow(BaseModel):
    """Row from private_content_collections for sync operations."""

    id: str
    external_id: str | None = None


class TemplateFavouriteRow(BaseModel):
    """Row from private_content_template_favourites."""

    id: str
    user_id: str
    template_id: str
    created_at: datetime | None = None


# ── Organizations ───────────────────────────────────────────────────────────


class OrgExistsRow(BaseModel):
    """Minimal org lookup to confirm existence."""

    id: str


# ── Assets ──────────────────────────────────────────────────────────────────


class AssetMetaRow(BaseModel):
    """Projection of assets table for type/storage lookups."""

    id: str
    asset_type: str | None = None
    storage_url: str | None = None
    storage_key: str | None = None


# ── Albums ──────────────────────────────────────────────────────────────────


class AlbumSummaryRow(BaseModel):
    """Projection of albums table for title/org lookups."""

    id: str
    title: str | None = None
    owner_org_id: str | None = None


class AlbumItemInsertRow(BaseModel):
    """Insert response for album_items."""

    id: str
    album_id: str | None = None
    asset_id: str | None = None
    created_at: datetime | None = None


# ── Notifications ───────────────────────────────────────────────────────────


class InternalNotificationInsertRow(BaseModel):
    """Insert response for internal_notifications."""

    id: str
    title: str | None = None
    body: str | None = None
    target_user_id: str | None = None
    org_id: str | None = None
    created_at: datetime | None = None


# ── Workflows ───────────────────────────────────────────────────────────────


class WorkflowBatchRunPatchRow(BaseModel):
    """Patch response for workflow_batch_runs status updates."""

    id: str
    status: str | None = None
    updated_at: datetime | None = None


class WorkflowToolsResponse(BaseModel):
    """Response model for the workflow tool definitions endpoint."""

    tools: list[dict[str, Any]]


# ── Schedule ────────────────────────────────────────────────────────────────


class ScheduleNotificationInsertRow(BaseModel):
    """Insert response for schedule-triggered notifications."""

    id: str
    created_at: datetime | None = None
