from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from .training import LoraTrainingOptions


class HealthStatus(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str | None = None
    value: Any | None = None
    result: Any | None = None
    auth: bool | None = None


class ServiceStatus(BaseModel):
    name: str
    status: str


class SystemHealthSummary(BaseModel):
    ok: bool
    services: list[ServiceStatus]
    timestamp: datetime | None = None
    uptime_ms: int | None = None


class SystemVersionResponse(BaseModel):
    version: str
    build: str | None = None


class NanoBananaOptions(BaseModel):
    sizes: list[str]
    pro_resolutions: list[str]
    aspect_ratios: list[str]
    max_reference_images: int = 10
    max_num_images: int = 10
    default_num_images: int = 1


class SeedreamOptions(BaseModel):
    image_sizes: list[str]
    image_resolutions: list[str]
    max_images: int = 6
    aspect_ratios: list[str] = []
    qualities: list[str] = []


class TopazOptions(BaseModel):
    image_upscale_factors: list[str] = ["1", "2", "4", "8"]
    video_upscale_factors: list[str] = ["1", "2", "4"]


class QwenOptions(BaseModel):
    job_types: list[str]
    model_names: list[str]
    tasks: list[str]
    inference_keys_by_job_type: dict[str, list[str]]
    max_reference_assets_by_job_type: dict[str, int] | None = None
    examples: list[dict[str, Any]] | None = None


class WanOptions(BaseModel):
    job_types: list[str]
    model_names: list[str]
    tasks: list[str]
    inference_keys_by_job_type: dict[str, list[str]]
    max_reference_assets_by_job_type: dict[str, int] | None = None
    defaults_by_job_type: dict[str, dict[str, Any]] | None = None
    resolution_presets_by_job_type: dict[str, list[dict[str, Any]]] | None = None


class FluxOptions(BaseModel):
    aspect_ratios: list[str] = []
    resolutions: list[str] = []
    max_reference_images: int = 8


class ZImageOptions(BaseModel):
    job_types: list[str]
    model_names: list[str]
    tasks: list[str]
    inference_keys_by_job_type: dict[str, list[str]]
    max_reference_assets_by_job_type: dict[str, int] | None = None


class SystemEnumsResponse(BaseModel):
    job_types: list[str]
    engine_types: list[str]
    engine_categories: list[str] | None = None
    engine_category_map: dict[str, list[str]] | None = None
    prompt_run_job_types: list[str] | None = None
    prompt_run_engine_types: list[str] | None = None
    prompt_template_schemas: list[dict[str, Any]] | None = None
    prompt_generators: list[dict[str, Any]] | None = None
    model_creation_modes: list[str] | None = None
    job_statuses: list[str]
    post_statuses: list[str]
    post_target_statuses: list[str]
    org_roles: list[str]
    grantee_types: list[str] | None = None
    resource_types: list[str] | None = None
    access_levels: list[str] | None = None
    membership_statuses: list[str] | None = None
    platforms: list[str]
    asset_types: list[str]
    lora_training: LoraTrainingOptions | None = None
    pipeline_base_models: list[str] | None = None
    pipeline_vae_models: list[str] | None = None
    pipeline_schedulers: list[str] | None = None
    pipeline_model_variants: list[str] | None = None
    pipeline_token_limits: dict[str, dict[str, int]] | None = None
    nanobanana_options: NanoBananaOptions | None = None
    seedream_options: SeedreamOptions | None = None
    topaz_options: TopazOptions | None = None
    qwen_options: QwenOptions | None = None
    wan_options: WanOptions | None = None
    zimage_options: ZImageOptions | None = None
    flux_options: FluxOptions | None = None
    job_type_titles: dict[str, str] | None = None
