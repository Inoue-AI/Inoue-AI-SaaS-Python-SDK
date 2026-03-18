from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .constants import RPC_CREATE_WEBHOOK_ENDPOINT
from .enums import JobStatus, ModelCreationMode, ModelJobType, ModelWorkflowStatus


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    registration_code: str | None = None
    referral_code: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    totp_code: str | None = None
    recovery_code: str | None = None


class RefreshRequest(BaseModel):
    refresh_token: str


class TwoFactorSetupRequest(BaseModel):
    user_id: str | None = None


class TwoFactorVerifyRequest(BaseModel):
    user_id: str | None = None
    code: str


class TwoFactorSetupResult(BaseModel):
    secret: str
    provisioning_uri: str
    recovery_codes: list[str]


class TwoFactorVerifyResult(BaseModel):
    verified: bool


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: User


class AccessTokenClaims(BaseModel):
    sub: str
    email: EmailStr
    role: str
    sid: str | None = None
    exp: int


class RefreshTokenClaims(BaseModel):
    sub: str
    type: str
    v: int
    sid: str | None = None
    exp: int


class WorkerTokenClaims(BaseModel):
    sub: str
    role: str
    exp: int


class User(BaseModel):
    id: str
    email: EmailStr
    display_name: str | None = None
    is_2fa_enabled: bool = False
    is_admin: bool = False
    roles: list[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_login_at: datetime | None = None


class AuthMeOrg(BaseModel):
    id: str
    name: str
    role: str
    icon_url: str | None = None
    status: str | None = None
    membership_id: str | None = None


class AuthMeResult(BaseModel):
    user: User
    orgs: list[AuthMeOrg]


class UserSessionResponse(BaseModel):
    id: str
    user_id: str
    device_name: str
    user_agent: str | None = None
    ip_address: str | None = None
    last_login_at: datetime | None = None
    last_activity_at: datetime | None = None
    revoked_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_current: bool = False


class UserSessionUpdateRequest(BaseModel):
    device_name: str = Field(min_length=1, max_length=120)


class UserSessionListQuery(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    include_revoked: bool = False


class UserSessionRevokeResponse(BaseModel):
    success: bool = True


class OrgCreateRequest(BaseModel):
    name: str
    icon_url: str | None = None


class OrgDeleteRequest(BaseModel):
    org_id: str


class OrgTransferRequest(BaseModel):
    org_id: str
    new_owner_user_id: str


class OrgMemberRemoveRequest(BaseModel):
    org_id: str
    user_id: str | None = None
    member_id: str | None = None


class OrgQuitRequest(BaseModel):
    org_id: str


class OrgResponse(BaseModel):
    id: str
    name: str
    icon_url: str | None = None
    owner_user_id: str | None = None
    created_at: datetime | None = None
    status: str | None = None
    membership_id: str | None = None


class OrgOverviewMember(BaseModel):
    id: str
    name: str
    role: str
    status: str


class OrgOverviewAudit(BaseModel):
    id: str
    action: str
    actor: str
    at: datetime
    trace_id: str | None = None


class OrgOverviewResponse(BaseModel):
    members: list[OrgOverviewMember]
    audits: list[OrgOverviewAudit]


class InviteRequest(BaseModel):
    org_id: str
    user_id: str | None = None
    email: EmailStr | None = None
    role: str = "member"


class RoleChangeRequest(BaseModel):
    org_id: str
    user_id: str
    role: str


class MembershipResponse(BaseModel):
    id: str | None = None
    org_id: str
    user_id: str
    role: str
    status: str
    email: str | None = None
    name: str | None = None
    created_at: datetime | None = None


class ModelCreateRequest(BaseModel):
    name: str
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    description: str | None = None
    creation_mode: ModelCreationMode | str = ModelCreationMode.BASE_TRAITS
    traits_spec: dict | None = None
    lora_upload_asset_id: str | None = None
    lora_upload_metadata: dict | None = None
    hf_repo_url: str | None = None
    hf_api_key_id: str | None = None


class ModelUpdateRequest(BaseModel):
    model_id: str
    name: str | None = None
    description: str | None = None
    canonical_face_image_url: str | None = None


class ModelForkRequest(BaseModel):
    model_id: str
    name: str | None = None
    owner_org_id: str | None = None
    owner_user_id: str | None = None


class ModelTransferRequest(BaseModel):
    model_id: str
    new_owner_user_id: str | None = None
    new_owner_org_id: str | None = None


class ModelShareRequest(BaseModel):
    model_id: str
    user_id: str | None = None
    org_id: str | None = None
    access_level: str = "view"


class ModelShareGrant(BaseModel):
    id: str | None = None
    resource_type: str
    resource_id: str
    grantee_type: str
    grantee_id: str
    access_level: str
    created_by_user_id: str
    target_name: str | None = None


class ModelResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str
    name: str
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    status: ModelWorkflowStatus | str | None = None
    description: str | None = None
    creation_mode: ModelCreationMode | str | None = None
    identity_ready: bool | None = None
    canonical_face_image_url: str | None = None
    canonical_body_image_url: str | None = None
    canonical_provenance: dict | None = None
    canonical_candidate_id: str | None = None
    canonical_source: str | None = None
    identity_lora_artifact_id: str | None = None
    base_lora_id: str | None = None
    traits_spec: dict | None = None
    lora_upload_asset_id: str | None = None
    lora_upload_metadata: dict | None = None
    hf_repo_url: str | None = None
    hf_api_key_id: str | None = None
    hf_repo_is_private: bool | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None
    stats: dict | None = None


class DatasetImagePayload(BaseModel):
    file_url: str
    file_sha256: str | None = None
    mime_type: str | None = None
    width: int | None = None
    height: int | None = None
    labels: list[str] | None = None
    stage_index: int | None = None
    metadata: dict | None = None


class DatasetImageUploadRequest(BaseModel):
    images: list[DatasetImagePayload] = Field(..., min_length=1, max_length=120)


class ModelDatasetImageResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    model_id: str
    file_url: str
    file_sha256: str | None = None
    mime_type: str | None = None
    width: int | None = None
    height: int | None = None
    labels: list[str] | None = None
    stage_index: int | None = None
    metadata: dict | None = Field(default=None, alias="metadata_json")
    created_at: datetime | None = None


class TrainingStageConfig(BaseModel):
    stage_index: int = Field(..., ge=1)
    name: str | None = None
    config: dict = Field(default_factory=dict)
    dataset_image_ids: list[str] | None = None


class TrainLoraJobRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    framework: str = "diffusers"
    script: str = "dreambooth_lora_sdxl"
    training_config: dict = Field(default_factory=dict, alias="trainingConfig")
    inference_config: dict | None = Field(default=None, alias="inferenceConfig")
    multi_stage: bool = False
    stage_count: int | None = None
    share_config_across_stages: bool = True
    stages: list[TrainingStageConfig] = Field(default_factory=list)
    training_type: Literal["hyperlora", "lora_sdxl_dreambooth", "lora_qwen_image"] = "lora_sdxl_dreambooth"


class GenerateCandidatesRequest(BaseModel):
    n: int = Field(8, ge=1, le=32)
    prompt_template: str | None = None
    negative_prompt: str | None = None
    scheduler: str | None = None
    seed_strategy: str = "random"
    fixed_seed: int | None = None


class ModelJobResponse(BaseModel):
    id: str
    model_id: str
    job_type: ModelJobType | str
    status: JobStatus | str
    progress: float | None = None
    payload: dict
    result: dict | None = None
    error: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ModelCandidateResponse(BaseModel):
    id: str
    model_id: str
    index: int
    face_image_url: str
    body_image_url: str
    provenance: dict
    created_at: datetime | None = None


class CanonicalSelectRequest(BaseModel):
    candidate_id: str


class GenerateAvatarRequest(BaseModel):
    era_preset_id: str
    prompt: str
    negative_prompt: str | None = None
    n_outputs: int = Field(1, ge=1, le=8)
    seed_strategy: str = "random"
    fixed_seed: int | None = None
    scheduler: str | None = None
    params: dict = Field(default_factory=dict)


class AvatarImageResponse(BaseModel):
    id: str
    avatar_id: str
    image_url: str
    index: int
    created_at: datetime | None = None


class AvatarResponse(BaseModel):
    id: str
    model_id: str
    era_preset_id: str
    prompt: str
    negative_prompt: str | None = None
    seed: int | None = None
    scheduler: str | None = None
    params: dict
    provenance: dict
    created_at: datetime | None = None
    images: list[AvatarImageResponse] = Field(default_factory=list)


class AvatarProfileCreateRequest(BaseModel):
    model_id: str
    name: str
    config: dict = Field(default_factory=dict)


class AvatarProfileResponse(BaseModel):
    id: str
    model_id: str
    name: str
    config_json: dict | None = None
    status: str | None = None


class PromptTemplateCreateRequest(BaseModel):
    title: str
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    description: str | None = None
    tags: list[str] = Field(default_factory=list)


class PromptOutputPreviewResponse(BaseModel):
    asset_id: str
    asset_url: str | None = None
    asset_type: str | None = None
    content_type: str | None = None
    run_id: str | None = None
    job_id: str | None = None
    created_at: datetime | None = None


class PromptTemplateResponse(BaseModel):
    id: str
    title: str
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    owner_email: EmailStr | None = None
    description: str | None = None
    tags: list[str] | None = None
    is_locked: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    linked_model_ids: list[str] | None = None
    latest_version_json: PromptVersionResponse | None = None
    example_outputs: list[PromptOutputPreviewResponse] = Field(default_factory=list)
    latest_run_outputs: list[PromptOutputPreviewResponse] = Field(default_factory=list)


class PromptVersionCreateRequest(BaseModel):
    template_id: str
    content: dict
    version_number: int | None = None


class PromptVersionResponse(BaseModel):
    id: str
    prompt_template_id: str
    version_number: int
    content_json: dict
    created_at: datetime | None = None


class PromptTemplateUpdateRequest(BaseModel):
    template_id: str
    title: str | None = None
    description: str | None = None
    tags: list[str] | None = None


class PromptTemplateExamplesUpdateRequest(BaseModel):
    asset_ids: list[str] = Field(default_factory=list, max_length=3)


class PromptTemplateDuplicateRequest(BaseModel):
    template_id: str
    title: str | None = None
    owner_user_id: str | None = None
    owner_org_id: str | None = None


class PromptTemplateModelLinkRequest(BaseModel):
    prompt_template_id: str = Field(validation_alias="template_id")
    model_id: str

    model_config = ConfigDict(populate_by_name=True)


class PromptTemplateModelLinkResponse(BaseModel):
    id: str
    prompt_template_id: str
    model_id: str


class PipelineCreateRequest(BaseModel):
    model_id: str
    created_by_user_id: str
    status: JobStatus = JobStatus.QUEUED


class PipelineResponse(BaseModel):
    id: str
    model_id: str | None = None
    status: JobStatus


class PromptRunCreateRequest(BaseModel):
    prompt_version_id: str
    model_id: str
    avatar_profile_id: str | None = None
    run_input_json: dict = Field(default_factory=dict)
    resolved_prompt_text: str
    engine_type: str = "seedream"
    engine_params_json: dict = Field(default_factory=dict)
    job_input: dict = Field(default_factory=dict)
    job_type: str = "seedream_v4_t2i"
    idempotency_key: str | None = None


class PromptRunResponse(BaseModel):
    id: str
    prompt_version_id: str
    model_id: str
    avatar_profile_id: str | None = None
    template_id: str | None = None
    template_title: str | None = None
    job_id: str | None = None
    output_preview: str | None = None
    resolved_prompt_text: str | None = None
    run_input_json: dict | None = None
    engine_params_json: dict | None = None
    engine_type: str | None = None
    job_type: str | None = None
    job_input_json: dict | None = None
    created_at: datetime | None = None
    status: JobStatus


class PromptRunBundleResponse(BaseModel):
    prompt_run: PromptRunResponse
    job: JobResponse
    pipeline_run: PipelineResponse


class JobCreateRequest(BaseModel):
    pipeline_run_id: str | None = None
    model_id: str
    prompt_run_id: str | None = None
    job_type: str
    input_json: dict = Field(default_factory=dict)
    status: JobStatus = JobStatus.QUEUED
    idempotency_key: str
    requested_by_user_id: str | None = None


class JobResponse(BaseModel):
    id: str
    model_id: str | None = None
    model_name: str | None = None
    pipeline_run_id: str | None = None
    prompt_run_id: str | None = None
    requested_by_user_id: str | None = None
    requested_by_email: str | None = None
    status: JobStatus
    job_type: str
    started_at: datetime | None = None
    claimed_at: datetime | None = None
    claimed_by_worker_id: str | None = None
    dispatched_at: datetime | None = None
    last_heartbeat_at: datetime | None = None
    input_json: dict | None = None
    finished_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    engine_type: str | None = None
    cost_credits: Decimal | None = None
    compute_seconds: int | None = None
    bill_failed_by_compute_seconds: bool | None = None
    progress_json: dict | None = None
    error_json: dict | None = None
    template_id: str | None = None
    template_title: str | None = None
    workflow_run_step_id: str | None = None


class JobStatusHistoryResponse(BaseModel):
    job_id: str
    new_status: JobStatus
    old_status: JobStatus
    changed_by_worker_id: str | None = None
    changed_at: datetime | None = None


class JobStatusHistoryCreateRequest(BaseModel):
    job_id: str
    old_status: JobStatus
    new_status: JobStatus
    changed_by_worker_id: str | None = None
    changed_at: datetime


class JobClaimRequest(BaseModel):
    pass


class JobClaimResponse(BaseModel):
    job_id: str
    status: JobStatus
    claimed_by_worker_id: str | None = None


class JobProgressRequest(BaseModel):
    progress_json: dict = Field(default_factory=dict)


class JobCompleteRequest(BaseModel):
    asset: dict | None = None
    assets: list[dict] | None = None
    provider_output_raw: dict | None = None


class JobFailRequest(BaseModel):
    error_json: dict | None = None


class AssetCreateRequest(BaseModel):
    asset_type: str
    origin_type: str
    owner_user_id: str | None = None
    owner_org_id: str | None = None
    storage_key: str
    storage_url: str | None = None
    storage_region: str | None = None
    storage_pod_id: str | None = None
    metadata_json: dict = Field(default_factory=dict)


class AssetResponse(BaseModel):
    id: str
    asset_type: str
    origin_type: str | None = None
    storage_key: str
    storage_url: str | None = None
    storage_region: str | None = None
    storage_pod_id: str | None = None
    owner_user_id: str | None = None
    owner_email: EmailStr | None = None
    owner_org_id: str | None = None
    metadata_json: dict | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class AssetPublicResponse(BaseModel):
    class LinkedModel(BaseModel):
        id: str
        name: str

    id: str
    asset_type: str
    origin_type: str | None = None
    storage_key: str | None = None
    storage_url: str | None = None
    public_url: str | None = None
    storage_region: str | None = None
    storage_pod_id: str | None = None
    owner_user_id: str | None = None
    owner_email: EmailStr | None = None
    owner_org_id: str | None = None
    metadata_json: dict | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    linked_models: list[LinkedModel] | None = None


class AssetUpdateRequest(BaseModel):
    title: str | None = None
    tags: list[str] | None = None
    notes: str | None = None
    archived: bool | None = None


class AssetBulkUpdateRequest(BaseModel):
    asset_ids: list[str]
    title: str | None = None
    tags: list[str] | None = None
    notes: str | None = None
    archived: bool | None = None


class AssetArchiveRequest(BaseModel):
    asset_id: str


class AssetPermadeleteRequest(BaseModel):
    asset_id: str


class AssetUnlinkRequest(BaseModel):
    asset_id: str
    model_id: str


class AssetLinkRequest(BaseModel):
    asset_id: str
    model_id: str


class AssetLinkResponse(BaseModel):
    id: str
    asset_id: str
    model_id: str
    linked_by_user_id: str | None = None


class AssetJobOutput(BaseModel):
    id: str
    job_id: str
    asset_id: str
    created_at: datetime | None = None


class CollectionCreateRequest(BaseModel):
    title: str
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    description: str | None = None


class CollectionResponse(BaseModel):
    id: str
    title: str
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    owner_email: EmailStr | None = None
    owner_name: str | None = None
    description: str | None = None
    linked_model_ids: list[str] | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class CollectionUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None


class CollectionItemCreateRequest(BaseModel):
    collection_id: str
    item_type: str = "link"
    title: str | None = None
    asset_id: str | None = None
    url: str | None = None
    note_text: str | None = None
    username: str | None = None
    password: str | None = None
    metadata_json: dict = Field(default_factory=dict)


class CollectionItemUpdateRequest(BaseModel):
    collection_id: str | None = None
    item_type: str | None = None
    title: str | None = None
    asset_id: str | None = None
    url: str | None = None
    note_text: str | None = None
    username: str | None = None
    password: str | None = None
    metadata_json: dict | None = None


class CollectionItemResponse(BaseModel):
    id: str
    collection_id: str
    item_type: str
    title: str | None = None
    url: str | None = None
    note_text: str | None = None
    username: str | None = None
    password: str | None = None
    has_password: bool | None = None
    metadata_json: dict | None = None
    created_at: datetime | None = None


class CollectionLinkRequest(BaseModel):
    collection_id: str
    model_id: str


class CollectionLinkResponse(BaseModel):
    id: str
    collection_id: str
    model_id: str


class CollectionItemRemoveRequest(BaseModel):
    item_id: str


class CollectionUnlinkRequest(BaseModel):
    collection_id: str
    model_id: str


class CollectionShareRequest(BaseModel):
    collection_id: str
    user_id: str | None = None
    org_id: str | None = None
    kind: str | None = None
    target: str | None = None
    access_level: str = "view"


class CollectionRevokeRequest(BaseModel):
    grant_id: str | None = None
    share_id: str | None = None


class CollectionDetailResponse(CollectionResponse):
    items: list[CollectionItemResponse] = Field(default_factory=list)


class AlbumCreateRequest(BaseModel):
    title: str
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    description: str | None = None


class AlbumResponse(BaseModel):
    id: str
    title: str
    owner_org_id: str | None = None
    owner_user_id: str | None = None
    owner_email: EmailStr | None = None
    owner_name: str | None = None
    description: str | None = None
    linked_model_ids: list[str] | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class AlbumUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None


class AlbumItemCreateRequest(BaseModel):
    album_id: str
    item_type: str = "link"
    title: str | None = None
    asset_id: str | None = None
    url: str | None = None
    note_text: str | None = None
    username: str | None = None
    password: str | None = None
    metadata_json: dict = Field(default_factory=dict)
    owner_org_id: str | None = None


class AlbumItemUpdateRequest(BaseModel):
    album_id: str | None = None
    item_type: str | None = None
    title: str | None = None
    asset_id: str | None = None
    url: str | None = None
    note_text: str | None = None
    username: str | None = None
    password: str | None = None
    metadata_json: dict | None = None


class AlbumItemResponse(BaseModel):
    id: str
    album_id: str
    item_type: str
    title: str | None = None
    asset_id: str | None = None
    url: str | None = None
    note_text: str | None = None
    username: str | None = None
    password: str | None = None
    has_password: bool | None = None
    metadata_json: dict | None = None
    created_at: datetime | None = None


class AlbumLinkRequest(BaseModel):
    album_id: str
    model_id: str


class AlbumLinkResponse(BaseModel):
    id: str
    album_id: str
    model_id: str


class AlbumItemRemoveRequest(BaseModel):
    item_id: str


class AlbumUnlinkRequest(BaseModel):
    album_id: str
    model_id: str


class AlbumShareRequest(BaseModel):
    album_id: str
    user_id: str | None = None
    org_id: str | None = None
    kind: str | None = None
    target: str | None = None
    access_level: str = "view"


class AlbumRevokeRequest(BaseModel):
    grant_id: str | None = None
    share_id: str | None = None


class AlbumDetailResponse(AlbumResponse):
    items: list[AlbumItemResponse] = Field(default_factory=list)


class HfKeyCreateRequest(BaseModel):
    label: str
    token: str


class HfKeyUpdateRequest(BaseModel):
    label: str | None = None


class HfKeyResponse(BaseModel):
    id: str
    label: str
    last4: str | None = None
    owner_user_id: str | None = None
    access_level: str | None = None
    can_manage: bool | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class CivitaiKeyCreateRequest(BaseModel):
    label: str
    token: str


class CivitaiKeyUpdateRequest(BaseModel):
    label: str | None = None


class CivitaiKeyResponse(BaseModel):
    id: str
    label: str
    last4: str | None = None
    owner_user_id: str | None = None
    access_level: str | None = None
    can_manage: bool | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ElevenLabsKeyCreateRequest(BaseModel):
    label: str
    token: str


class ElevenLabsKeyUpdateRequest(BaseModel):
    label: str | None = None


class ElevenLabsKeyResponse(BaseModel):
    id: str
    label: str
    last4: str | None = None
    owner_user_id: str | None = None
    access_level: str | None = None
    can_manage: bool | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class HfKeyShareRequest(BaseModel):
    key_id: str
    user_id: str | None = None
    org_id: str | None = None
    kind: str | None = None
    target: str | None = None
    access_level: str = "view"


class CivitaiKeyShareRequest(BaseModel):
    key_id: str
    user_id: str | None = None
    org_id: str | None = None
    kind: str | None = None
    target: str | None = None
    access_level: str = "view"


class ElevenLabsKeyShareRequest(BaseModel):
    key_id: str
    user_id: str | None = None
    org_id: str | None = None
    kind: str | None = None
    target: str | None = None
    access_level: str = "view"


class KeyShareRevokeRequest(BaseModel):
    grant_id: str | None = None
    share_id: str | None = None


class SavedLoraCreateRequest(BaseModel):
    label: str
    source: Literal["huggingface", "civitai"]
    weight_name: str | None = None
    scale: float | None = Field(default=1.0, gt=0)
    huggingface_repo_id: str | None = None
    hf_api_key_id: str | None = None
    civitai_model_version_id: str | None = None
    civitai_api_key_id: str | None = None


class SavedLoraUpdateRequest(BaseModel):
    label: str | None = None
    source: Literal["huggingface", "civitai"] | None = None
    weight_name: str | None = None
    scale: float | None = Field(default=None, gt=0)
    huggingface_repo_id: str | None = None
    hf_api_key_id: str | None = None
    civitai_model_version_id: str | None = None
    civitai_api_key_id: str | None = None


class SavedLoraResponse(BaseModel):
    id: str
    label: str
    source: Literal["huggingface", "civitai"]
    weight_name: str | None = None
    scale: float | None = None
    huggingface_repo_id: str | None = None
    hf_api_key_id: str | None = None
    civitai_model_version_id: str | None = None
    civitai_api_key_id: str | None = None
    owner_user_id: str | None = None
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class PostTarget(BaseModel):
    platform: str
    connected_account_id: str | None = None
    status: str | None = None
    publish_at: datetime | None = None
    preview_payload: dict | None = None


class PostCreateRequest(BaseModel):
    org_id: str
    model_id: str
    body_text: str
    publish_at: datetime | None = None
    attachments: list[str] = Field(default_factory=list)
    targets: list[PostTarget] = Field(default_factory=list)
    preview_payload: dict | None = None


class PostResponse(BaseModel):
    id: str
    model_id: str
    body_text: str | None = None
    status: str | None = None
    publish_at: datetime | None = None
    preview_payload: dict | None = None


class ApproveRequest(BaseModel):
    post_id: str
    org_id: str


class PostingPolicyRequest(BaseModel):
    org_id: str
    requires_approval: bool = True


class PostingPolicyResponse(BaseModel):
    org_id: str
    requires_approval: bool


class PublishRequest(BaseModel):
    post_id: str
    org_id: str
    publish_at: datetime | None = None


class WebhookEndpointCreateRequest(BaseModel):
    connected_account_id: str
    url: str
    secret: str | None = None


class FanvueConnectCallbackRequest(BaseModel):
    code: str


class WebhookEndpointResponse(BaseModel):
    endpoint_id: str = Field(..., alias=RPC_CREATE_WEBHOOK_ENDPOINT)
    secret: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class WebhookIngestRequest(BaseModel):
    endpoint_id: str
    payload: dict
    event_type: str = "unknown"


class WebhookEventResponse(BaseModel):
    id: str
    platform: str
    endpoint_id: str
    event_type: str
    raw_payload: dict


class WorkerRegisterRequest(BaseModel):
    # Optional explicit worker ID (UUID). If omitted the backend will generate one.
    id: str | None = None
    name: str = "worker"


class WorkerRegisterResponse(BaseModel):
    id: str
    name: str
    status: str
    updated_at: datetime | None = None


class WorkerTokenRequest(BaseModel):
    worker_id: str


class WorkerTokenResponse(BaseModel):
    worker_token: str


# Forward references
TokenPairResponse.model_rebuild()
PromptTemplateResponse.model_rebuild()
