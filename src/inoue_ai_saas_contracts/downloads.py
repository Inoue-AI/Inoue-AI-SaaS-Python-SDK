from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .auth import AssetPublicResponse
from .enums import JobStatus


class ContentDownloadCreateRequest(BaseModel):
    url: str = Field(min_length=1, max_length=4096)
    owner_org_id: str | None = None
    model_id: str | None = None
    album_ids: list[str] | None = None
    idempotency_key: str | None = Field(default=None, max_length=255)


class ContentDownloadBatchItemRequest(BaseModel):
    url: str = Field(min_length=1, max_length=4096)
    idempotency_key: str | None = Field(default=None, max_length=255)


class ContentDownloadBatchCreateRequest(BaseModel):
    owner_org_id: str | None = None
    model_id: str | None = None
    album_ids: list[str] | None = None
    idempotency_key: str | None = Field(default=None, max_length=255)
    items: list[ContentDownloadBatchItemRequest] = Field(min_length=1, max_length=100)


class ContentDownloadListQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    status: JobStatus | str | None = None
    platform: str | None = None
    provider: str | None = None
    model_id: str | None = None
    batch_id: str | None = None
    owner_org_id: str | None = None


class ContentDownloadResponse(BaseModel):
    id: str
    batch_id: str | None = None
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    model_id: str | None = None
    requested_by_user_id: str | None = None
    url: str
    platform: str
    provider: str
    status: JobStatus
    idempotency_key: str | None = None
    progress_json: dict[str, Any] | None = None
    error_json: dict[str, Any] | None = None
    metadata_json: dict[str, Any] | None = None
    started_at: datetime | None = None
    claimed_at: datetime | None = None
    claimed_by_worker_id: str | None = None
    dispatched_at: datetime | None = None
    last_heartbeat_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ContentDownloadBatchCreateResult(BaseModel):
    batch_id: str
    items: list[ContentDownloadResponse]


class ContentDownloadCancelRequest(BaseModel):
    download_id: str


class ContentDownloadRetryRequest(BaseModel):
    download_id: str


class ContentDownloadDeleteRequest(BaseModel):
    download_id: str


class ContentDownloadStatusHistoryResponse(BaseModel):
    download_id: str
    new_status: JobStatus
    old_status: JobStatus
    changed_by_worker_id: str | None = None
    changed_at: datetime | None = None


class ContentDownloadStatusHistoryCreateRequest(BaseModel):
    download_id: str
    old_status: JobStatus
    new_status: JobStatus
    changed_by_worker_id: str | None = None
    changed_at: datetime


class ContentDownloadAssetOutput(BaseModel):
    id: str
    download_id: str
    asset_id: str
    metadata_json: dict[str, Any] | None = None
    created_at: datetime | None = None


class ContentDownloadOutputResponse(BaseModel):
    id: str
    download_id: str
    asset_id: str
    metadata_json: dict[str, Any] | None = None
    created_at: datetime | None = None
    asset: AssetPublicResponse | None = None


class AdminDownloadProviderSettingResponse(BaseModel):
    platform: str
    provider: str | None = None
    supported_providers: list[str] = Field(default_factory=list)
    updated_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AdminDownloadProviderSettingUpdateRequest(BaseModel):
    provider: str = Field(min_length=1, max_length=255)


class ContentDownloadClaimResponse(BaseModel):
    download_id: str
    status: JobStatus
    claimed_by_worker_id: str | None = None


class ContentDownloadProgressRequest(BaseModel):
    progress_json: dict[str, Any] = Field(default_factory=dict)


class ContentDownloadAssetPayload(BaseModel):
    asset_type: str
    storage_key: str
    storage_url: str | None = None
    storage_region: str | None = None
    storage_pod_id: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class ContentDownloadCompleteRequest(BaseModel):
    assets: list[ContentDownloadAssetPayload] = Field(default_factory=list)
    metadata_json: dict[str, Any] | None = None
    progress_json: dict[str, Any] | None = None


class ContentDownloadFailRequest(BaseModel):
    error_json: dict[str, Any] | None = None
    progress_json: dict[str, Any] | None = None


class ContentDownloadCompletionResult(BaseModel):
    download: ContentDownloadResponse
    asset_ids: list[str] | None = None
