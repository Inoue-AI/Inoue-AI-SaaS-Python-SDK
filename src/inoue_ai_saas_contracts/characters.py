from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .pagination import DateRangeQuery, PaginationQuery


class CharacterGenerationOptions(BaseModel):
    job_type: str = "nanobanana_pro_t2i_4k"
    aspect_ratio: str = "9:16"
    resolution: str = "4K"
    size: str | None = None
    quality: str | None = None
    jobs_count: int = Field(default=4, ge=1, le=10)
    num_images_per_job: int = Field(default=1, ge=1, le=10)
    reference_asset_ids: list[str] | None = None
    reference_image_urls: list[str] | None = None


class CharacterCreationRequest(BaseModel):
    model_id: str | None = None
    owner_org_id: str | None = None
    title: str | None = None
    is_saved: bool = False
    config_json: dict[str, Any] = Field(default_factory=dict)
    generation: CharacterGenerationOptions = Field(default_factory=CharacterGenerationOptions)


class CharacterCreationUpdateRequest(BaseModel):
    title: str | None = None
    is_saved: bool | None = None


class CharacterCreationListQuery(PaginationQuery, DateRangeQuery):
    model_id: str | None = None
    org_id: str | None = None
    saved_only: bool | None = None
    q: str | None = None


class CharacterCreationResponse(BaseModel):
    id: str
    owner_user_id: str | None = None
    owner_org_id: str | None = None
    created_by_user_id: str | None = None
    model_id: str | None = None
    title: str | None = None
    is_saved: bool = False
    config_json: dict[str, Any] = Field(default_factory=dict)
    generation_json: dict[str, Any] = Field(default_factory=dict)
    prompt_text: str
    job_type: str
    jobs_count: int = 1
    job_ids: list[str] = Field(default_factory=list)
    latest_job_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CharacterCreationEnqueueResponse(BaseModel):
    creation: CharacterCreationResponse
    jobs: list[Any] = Field(default_factory=list)


class CharacterPromptSchemaResponse(BaseModel):
    schema: dict[str, Any]
