"""Vision and generation endpoint contracts."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .enums import JobType


class FaceSwapRequest(BaseModel):
    model_id: str | None = None
    owner_org_id: str | None = None
    source_asset_id: str
    target_asset_ids: list[str]
    swap_id: str | None = None
    options: dict[str, Any] | None = None
    output_prefix: str | None = None


class CropAssetItem(BaseModel):
    asset_id: str
    category: str | None = None
    sizes: list[int] | None = None


class ImageCropRequest(BaseModel):
    model_id: str
    owner_org_id: str | None = None
    dataset: list[CropAssetItem] = Field(default_factory=list)
    crop_id: str | None = None
    pad_mode: str | None = None
    pad_constant: int | None = None
    crop_ui: bool | None = None
    output_format: str | None = None
    jpeg_quality: int | None = None
    sizes: list[int] | None = None
    category: str | None = None
    output_prefix: str | None = None


class SeedreamRequest(BaseModel):
    model_id: str | None = None
    owner_org_id: str | None = None
    job_type: JobType
    prompt: str
    image_size: str | None = None
    image_resolution: str | None = None
    max_images: int | None = None
    seed: int | None = None
    aspect_ratio: str | None = None
    quality: str | None = None
    reference_asset_ids: list[str] | None = None
    reference_image_urls: list[str] | None = None
    idempotency_key: str | None = None
    output_prefix: str | None = None
    prompt_run_id: str | None = None
    prompt_version_id: str | None = None


class TopazRequest(BaseModel):
    model_id: str | None = None
    owner_org_id: str | None = None
    job_type: JobType
    reference_asset_id: str
    upscale_factor: str | int = "2"
    idempotency_key: str | None = None
    output_prefix: str | None = None
    prompt_run_id: str | None = None
    prompt_version_id: str | None = None


class NanoBananaRequest(BaseModel):
    model_id: str | None = None
    owner_org_id: str | None = None
    job_type: JobType
    prompt: str
    num_images: int = Field(default=1, ge=1)
    size: str | None = None
    resolution: str | None = None
    aspect_ratio: str | None = None
    reference_asset_ids: list[str] | None = None
    reference_image_urls: list[str] | None = None
    idempotency_key: str | None = None
    output_prefix: str | None = None
    prompt_run_id: str | None = None
    prompt_version_id: str | None = None


class SoraRequest(BaseModel):
    model_id: str | None = None
    owner_org_id: str | None = None
    job_type: JobType
    prompt: str
    length_seconds: int = Field(default=4, ge=1, le=60)
    aspect_ratio: str
    resolution: str | None = None
    reference_asset_id: str | None = None
    idempotency_key: str | None = None
    output_prefix: str | None = None
    prompt_run_id: str | None = None
    prompt_version_id: str | None = None


class KlingRequest(BaseModel):
    model_id: str | None = None
    owner_org_id: str | None = None
    job_type: JobType
    prompt: str | None = None
    length_seconds: int = Field(default=4, ge=1, le=60)
    aspect_ratio: str | None = None
    generate_audio: bool | None = None
    mode: str | None = None
    negative_prompt: str | None = None
    strength: float | int | None = None
    reference_asset_ids: list[str] | None = None
    reference_video_asset_id: str | None = None
    character_orientation: str | None = None
    tail_asset_id: str | None = None
    multi_shots: bool | None = None
    multi_prompt: list[dict[str, Any]] | None = None
    sound: bool | None = None
    image_urls: list[str] | None = None
    kling_elements: list[dict[str, Any]] | None = None
    idempotency_key: str | None = None
    output_prefix: str | None = None
    prompt_run_id: str | None = None
    prompt_version_id: str | None = None


class GrokRequest(BaseModel):
    model_id: str | None = None
    owner_org_id: str | None = None
    job_type: JobType
    prompt: str
    aspect_ratio: str | None = None
    mode: str | None = None
    duration: int | str | None = None
    resolution: str | None = None
    image_urls: list[str] | None = None
    reference_asset_id: str | None = None
    task_id: str | None = None
    index: int | None = None
    idempotency_key: str | None = None
    output_prefix: str | None = None
    prompt_run_id: str | None = None
    prompt_version_id: str | None = None


class FluxRequest(BaseModel):
    model_id: str | None = None
    owner_org_id: str | None = None
    job_type: JobType
    prompt: str
    aspect_ratio: str | None = None
    resolution: str | None = None
    reference_asset_ids: list[str] | None = None
    reference_image_urls: list[str] | None = None
    idempotency_key: str | None = None
    output_prefix: str | None = None
    prompt_run_id: str | None = None
    prompt_version_id: str | None = None
