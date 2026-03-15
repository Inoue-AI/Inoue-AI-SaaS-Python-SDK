from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .auth import JobResponse
from .enums import JobType


class BaseJobPayload(BaseModel):
    job_type: JobType
    input_json: dict[str, Any] = Field(default_factory=dict)


class SdxlImageJobPayload(BaseJobPayload):
    width: int | None = None
    height: int | None = None
    prompt: str | None = None
    negative_prompt: str | None = None


class FanvueUploadJobPayload(BaseJobPayload):
    asset_storage_key: str
    caption: str | None = None


class GenericJobPayload(BaseJobPayload):
    """Fallback job payload for loosely typed jobs."""

    pass


class JobCompletionResult(BaseModel):
    job: JobResponse
    asset_id: str | None = None
    asset_ids: list[str] | None = None
