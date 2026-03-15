from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class LoraTrainingFieldOption(BaseModel):
    value: str
    label: str
    description: str | None = None
    example: str | None = None


class LoraTrainingField(BaseModel):
    key: str
    label: str
    input_type: str
    description: str
    required: bool = False
    placeholder: str | None = None
    default: Any | None = None
    example: Any | None = None
    min: float | None = None
    max: float | None = None
    step: float | None = None
    options: list[LoraTrainingFieldOption] | None = None


class LoraTrainingScript(BaseModel):
    id: str
    label: str
    framework: str
    description: str
    supports_multi_stage: bool = True
    fields: list[LoraTrainingField] = Field(default_factory=list)


class LoraTrainingOptions(BaseModel):
    frameworks: list[str]
    scripts: list[LoraTrainingScript]
