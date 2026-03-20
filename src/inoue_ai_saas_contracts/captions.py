"""Contracts for caption projects, transcription requests, and caption render requests."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .enums import JobStatus

# ── Caption Project ──


class CaptionProjectResponse(BaseModel):
    id: str
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    created_by_user_id: str | None = None
    title: str = ""
    source_asset_id: str | None = None
    source_asset_url: str | None = None
    template_name: str = "Matt"
    config_style: dict[str, Any] = Field(default_factory=dict)
    highlight_style: dict[str, Any] = Field(default_factory=dict)
    subs_config: dict[str, Any] = Field(default_factory=dict)
    input_props: dict[str, Any] = Field(default_factory=dict)
    words_json: list[dict[str, Any]] | None = None
    chunks_json: list[dict[str, Any]] | None = None
    language_detected: str | None = None
    duration_seconds: float | None = None
    fps: int = 30
    width: int = 720
    height: int = 1280
    display_watermark: bool = False
    status: str = "draft"
    metadata_json: dict[str, Any] | None = None
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CaptionProjectCreateRequest(BaseModel):
    title: str = ""
    source_asset_id: str | None = None
    source_asset_url: str | None = None
    template_name: str = "Matt"
    config_style: dict[str, Any] = Field(default_factory=dict)
    highlight_style: dict[str, Any] = Field(default_factory=dict)
    subs_config: dict[str, Any] = Field(default_factory=dict)
    fps: int = 30
    width: int = 720
    height: int = 1280
    display_watermark: bool = False
    language_hint: str | None = None
    provider: str = "deepgram"
    owner_org_id: str | None = None
    metadata_json: dict[str, Any] | None = None


class CaptionProjectUpdateRequest(BaseModel):
    title: str | None = None
    template_name: str | None = None
    config_style: dict[str, Any] | None = None
    highlight_style: dict[str, Any] | None = None
    subs_config: dict[str, Any] | None = None
    input_props: dict[str, Any] | None = None
    words_json: list[dict[str, Any]] | None = None
    chunks_json: list[dict[str, Any]] | None = None
    fps: int | None = None
    width: int | None = None
    height: int | None = None
    display_watermark: bool | None = None
    metadata_json: dict[str, Any] | None = None


class CaptionProjectListQuery(BaseModel):
    owner_org_id: str | None = None
    status: str | None = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class CaptionProjectExportRequest(BaseModel):
    """Request to start a caption render (export) for a project."""

    quality: str = "720p"
    fps: int | None = None
    codec: str = "h264"


# ── Transcription Request ──


class TranscriptionRequestResponse(BaseModel):
    id: str
    caption_project_id: str
    asset_id: str | None = None
    asset_url: str | None = None
    status: JobStatus
    language_hint: str | None = None
    provider: str = "deepgram"
    claimed_by_worker_id: str | None = None
    claimed_at: datetime | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    last_heartbeat_at: datetime | None = None
    dispatched_at: datetime | None = None
    progress_json: dict[str, Any] | None = None
    error_json: dict[str, Any] | None = None
    words_json: list[dict[str, Any]] | None = None
    chunks_json: list[dict[str, Any]] | None = None
    language_detected: str | None = None
    duration_seconds: float | None = None
    metadata_json: dict[str, Any] | None = None
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TranscriptionClaimResponse(BaseModel):
    id: str
    status: JobStatus
    claimed_by_worker_id: str | None = None
    claimed_at: datetime | None = None


class TranscriptionProgressRequest(BaseModel):
    progress_json: dict[str, Any] = Field(default_factory=dict)


class TranscriptionCompleteRequest(BaseModel):
    words_json: list[dict[str, Any]] = Field(default_factory=list)
    chunks_json: list[dict[str, Any]] = Field(default_factory=list)
    language_detected: str = ""
    duration_seconds: float = 0.0


class TranscriptionFailRequest(BaseModel):
    error_json: dict[str, Any] | None = None


class TranscriptionStatusHistoryResponse(BaseModel):
    transcription_request_id: str
    new_status: JobStatus
    old_status: JobStatus
    changed_by_worker_id: str | None = None
    changed_at: datetime | None = None


class TranscriptionStatusHistoryCreateRequest(BaseModel):
    transcription_request_id: str
    old_status: JobStatus
    new_status: JobStatus
    changed_by_worker_id: str | None = None
    changed_at: datetime


# ── Caption Render Request ──


class CaptionRenderRequestResponse(BaseModel):
    id: str
    caption_project_id: str
    source_asset_url: str | None = None
    input_props: dict[str, Any] = Field(default_factory=dict)
    quality: str = "720p"
    fps: int = 30
    codec: str = "h264"
    status: JobStatus
    claimed_by_worker_id: str | None = None
    claimed_at: datetime | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    last_heartbeat_at: datetime | None = None
    dispatched_at: datetime | None = None
    progress_json: dict[str, Any] | None = None
    error_json: dict[str, Any] | None = None
    output_url: str | None = None
    output_bucket: str | None = None
    output_key: str | None = None
    metadata_json: dict[str, Any] | None = None
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CaptionRenderClaimResponse(BaseModel):
    id: str
    status: JobStatus
    claimed_by_worker_id: str | None = None
    claimed_at: datetime | None = None


class CaptionRenderProgressRequest(BaseModel):
    progress_json: dict[str, Any] = Field(default_factory=dict)


class CaptionRenderCompleteRequest(BaseModel):
    output_url: str
    output_bucket: str
    output_key: str


class CaptionRenderFailRequest(BaseModel):
    error_json: dict[str, Any] | None = None


class CaptionRenderStatusHistoryResponse(BaseModel):
    caption_render_request_id: str
    new_status: JobStatus
    old_status: JobStatus
    changed_by_worker_id: str | None = None
    changed_at: datetime | None = None


class CaptionRenderStatusHistoryCreateRequest(BaseModel):
    caption_render_request_id: str
    old_status: JobStatus
    new_status: JobStatus
    changed_by_worker_id: str | None = None
    changed_at: datetime
