"""ElevenLabs voice and TTS contracts."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .pagination import PaginationQuery


class ElevenLabsModelsQuery(BaseModel):
    key_id: str


class ElevenLabsModelResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    model_id: str | None = None
    name: str | None = None
    can_do_text_to_speech: bool | None = None


class ElevenLabsVoiceListQuery(PaginationQuery):
    key_id: str
    model_id: str | None = None
    search: str | None = None


class ElevenLabsVoiceGetQuery(BaseModel):
    key_id: str


class ElevenLabsVoiceModelLinksQuery(BaseModel):
    key_id: str


class ElevenLabsVoiceModelLinksUpdateRequest(BaseModel):
    key_id: str
    model_ids: list[str] = Field(default_factory=list)


class ElevenLabsVoiceFileInput(BaseModel):
    name: str | None = None
    mime_type: str | None = None
    content_base64: str | None = None
    url: str | None = None


class ElevenLabsVoiceCloneRequest(BaseModel):
    key_id: str
    name: str
    files: list[ElevenLabsVoiceFileInput] = Field(default_factory=list)
    asset_ids: list[str] = Field(default_factory=list)
    remove_background_noise: bool | None = None
    description: str | None = None
    labels: dict[str, str | None] | None = None
    model_ids: list[str] = Field(default_factory=list)


class ElevenLabsVoiceDesignRequest(BaseModel):
    key_id: str
    voice_name: str
    voice_description: str
    output_format: str | None = None
    model_id: str | None = None
    text: str | None = None
    labels: dict[str, str | None] | None = None
    generated_voice_id: str | None = None
    preview_index: int = 0
    model_ids: list[str] = Field(default_factory=list)


class ElevenLabsVoiceUpdateRequest(BaseModel):
    key_id: str
    name: str | None = None
    description: str | None = None
    remove_background_noise: bool | None = None
    labels: dict[str, str | None] | None = None
    files: list[ElevenLabsVoiceFileInput] = Field(default_factory=list)
    asset_ids: list[str] = Field(default_factory=list)
    model_ids: list[str] | None = None


class ElevenLabsVoiceSettingsUpdateRequest(BaseModel):
    key_id: str
    settings: dict[str, Any]


class ElevenLabsTtsRequest(BaseModel):
    key_id: str
    model_id: str
    voice_id: str
    text: str
    elevenlabs_model_id: str = "eleven_multilingual_v2"
    output_format: str | None = None
    enable_logging: bool | None = None
    optimize_streaming_latency: int | None = None
    seed: int | None = None
    language_code: str | None = None
    previous_text: str | None = None
    next_text: str | None = None
    previous_request_ids: list[str] | None = None
    next_request_ids: list[str] | None = None
    use_pvc_as_ivc: bool | None = None
    apply_text_normalization: str | None = None
    enable_ssml_parsing: bool | None = None
    pronunciation_dictionary_locators: list[dict[str, Any]] | None = None
    voice_settings: dict[str, Any] | None = None


class ElevenLabsSpeechResponse(BaseModel):
    audio_base64: str
    mime_type: str | None = None
    voice_id: str
    model_id: str | None = None
    output_format: str | None = None


class ElevenLabsVoiceResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    voice_id: str
    name: str | None = None
    category: str | None = None
    description: str | None = None
    labels: dict[str, Any] | None = None
    preview_url: str | None = None
    settings: dict[str, Any] | None = None
    raw: dict[str, Any] | None = None
    model_ids: list[str] = Field(default_factory=list)
    model_names: list[str] = Field(default_factory=list)


class ElevenLabsVoiceDesignResponse(BaseModel):
    generated_voice_id: str | None = None
    previews: list[dict[str, Any]] = Field(default_factory=list)
    voice: ElevenLabsVoiceResponse
