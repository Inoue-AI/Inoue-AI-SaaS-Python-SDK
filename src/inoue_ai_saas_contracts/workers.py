from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .enums import JobStatus


class WorkerTokenClaims(BaseModel):
    sub: str
    role: str
    exp: int
    email: str | None = None


class JobClaimRequest(BaseModel):
    pass


class JobClaimResponse(BaseModel):
    job_id: str
    status: JobStatus
    claimed_by_worker_id: str | None = None


class JobProgressRequest(BaseModel):
    progress_json: dict[str, Any] = Field(default_factory=dict)


class JobCompleteRequest(BaseModel):
    asset: dict[str, Any] | None = None
    assets: list[dict[str, Any]] | None = None
    provider_output_raw: dict[str, Any] | None = None


class JobFailRequest(BaseModel):
    error_json: dict[str, Any] | None = None


class WorkerStatusRequest(BaseModel):
    status: str


class ReleaseDeadClaimsRequest(BaseModel):
    worker_liveness_seconds: int = 120
    limit: int = 50


class ReleaseDeadClaimsResponse(BaseModel):
    released_count: int = 0
    released_job_ids: list[str] | None = None
    dead_worker_ids: list[str] | None = None


class AssetUploadMessage(BaseModel):
    asset_id: str
    storage_key: str
    storage_url: str
    bucket: str
    local_path: str
    region: str | None = None
    endpoint: str | None = None
    pod_id: str | None = None
    content_type: str | None = None
    size_bytes: int | None = None
    delete_after_upload: bool = True
