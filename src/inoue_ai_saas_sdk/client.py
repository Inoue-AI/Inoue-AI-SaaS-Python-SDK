from __future__ import annotations

import uuid
from collections.abc import Mapping
from email.utils import parsedate_to_datetime
from typing import Any, TypeVar

import httpx
import inoue_ai_saas_contracts as contracts
from httpx import AsyncClient
from inoue_ai_saas_contracts.constants import (
    API_PREFIX,
    HEADER_ADMIN_TOKEN,
    HEADER_TRACE_ID,
    HEADER_WORKER_BOOTSTRAP,
    INTERNAL_PREFIX,
)
from inoue_ai_saas_contracts.enums import ErrorCode
from inoue_ai_saas_contracts.responses import ErrorBody, ResponseMeta
from pydantic import BaseModel, TypeAdapter, ValidationError

from .exceptions import SdkError, SdkTransportError
from .models import (
    AcceptedResult,
    ApiResult,
    ApprovedResult,
    AssetPublicResponse,
    AuthMeResult,
    DeclinedResult,
    DeletionResult,
    DeniedResult,
    HealthStatus,
    JobCompletionResult,
    ModelIdentityMapRequest,
    ModelShareGrant,
    MutedResult,
    NotificationItem,
    OrgOverviewResponse,
    QuitResult,
    ReadResult,
    RevenueSummary,
    RevokedResult,
    TwoFactorSetupResult,
    TwoFactorVerifyResult,
    UnlockedResult,
    UnmutedResult,
    UnreadResult,
    WebhookEndpointCreateResult,
    WebhookIngestResult,
)

T = TypeVar("T")


def _type_adapter(model: Any) -> TypeAdapter[Any]:
    return TypeAdapter(model)


def _normalize_headers(headers: Mapping[str, str] | None) -> dict[str, str]:
    return {k: v for k, v in (headers or {}).items()}


def _coerce_datetimes(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _coerce_datetimes(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_coerce_datetimes(item) for item in value]
    if isinstance(value, str):
        try:
            parsed = parsedate_to_datetime(value)
        except (TypeError, ValueError, IndexError):
            return value
        return parsed
    return value


class _ServiceBase:
    def __init__(self, client: InoueAiSaasClient):
        self._client = client

    def _payload(
        self, model: type[BaseModel], provided: BaseModel | Mapping[str, Any] | None, **kwargs: Any
    ) -> dict[str, Any]:
        return self._client._build_payload(model, provided, **kwargs)


class InoueAiSaasClient:
    def __init__(
        self,
        base_url: str,
        *,
        access_token: str | None = None,
        timeout: float | httpx.Timeout | None = 30.0,
        default_headers: Mapping[str, str] | None = None,
        webhooks_base_url: str | None = None,
        webhooks_headers: Mapping[str, str] | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        webhooks_transport: httpx.AsyncBaseTransport | None = None,
    ):
        self._client = AsyncClient(
            base_url=base_url, timeout=timeout, headers=_normalize_headers(default_headers), transport=transport
        )
        self._webhooks_client = AsyncClient(
            base_url=webhooks_base_url or base_url,
            timeout=timeout,
            headers=_normalize_headers(webhooks_headers or default_headers),
            transport=webhooks_transport or transport,
        )
        self._access_token = access_token
        self._refresh_token: str | None = None

        self.auth = AuthApi(self)
        self.orgs = OrgsApi(self)
        self.models = ModelsApi(self)
        self.prompts = PromptsApi(self)
        self.jobs = JobsApi(self)
        self.downloads = DownloadsApi(self)
        self.credits = CreditsApi(self)
        self.billing = BillingApi(self)
        self.admin_downloads = AdminDownloadsApi(self)
        self.internal = InternalApi(self)
        self.assets = AssetsApi(self)
        self.posts = PostsApi(self)
        self.schedule = ScheduleApi(self)
        self.calendar_feeds = CalendarFeedsApi(self)
        self.webhooks = WebhooksApi(self)
        self.threads = ThreadsApi(self)
        self.collections = CollectionsApi(self)
        self.pooling = PoolingApi(self)
        self.notifications = NotificationsApi(self)
        self.analytics = AnalyticsApi(self)
        self.audit = AuditApi(self)
        self.system = SystemApi(self)
        self.workflows = WorkflowsApi(self)
        self.push_subscriptions = PushSubscriptionsApi(self)
        self.albums = AlbumsApi(self)
        self.vision = VisionApi(self)
        self.tiktok = TikTokApi(self)
        self.referrals = ReferralsApi(self)
        self.huggingface = HuggingFaceApi(self)
        self.civitai = CivitaiApi(self)
        self.elevenlabs = ElevenLabsApi(self)
        self.legal = LegalApi(self)
        self.apps = AppsApi(self)
        self.discord_webhooks = DiscordWebhooksApi(self)

    @property
    def access_token(self) -> str | None:
        return self._access_token

    @property
    def refresh_token(self) -> str | None:
        return self._refresh_token

    def set_access_token(self, token: str | None) -> None:
        self._access_token = token

    def set_refresh_token(self, token: str | None) -> None:
        self._refresh_token = token

    def set_token_pair(self, tokens: contracts.TokenPairResponse) -> None:
        self._access_token = tokens.access_token
        self._refresh_token = tokens.refresh_token

    async def __aenter__(self) -> InoueAiSaasClient:
        await self._client.__aenter__()
        await self._webhooks_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()
        await self._webhooks_client.aclose()

    async def health(self, headers: Mapping[str, str] | None = None) -> ApiResult[HealthStatus]:
        return await self._request("GET", "/health", headers=headers, response_model=HealthStatus)

    def _build_payload(
        self, model: type[BaseModel], provided: BaseModel | Mapping[str, Any] | None, **kwargs: Any
    ) -> dict[str, Any]:
        if provided is None and not kwargs:
            return {}
        if provided is None:
            instance = model.model_validate(kwargs)
        elif isinstance(provided, BaseModel):
            instance = provided
        else:
            instance = model.model_validate(provided)
        return instance.model_dump(exclude_none=True, by_alias=True)

    def _prepare_headers(
        self,
        *,
        client_headers: Mapping[str, str],
        headers: Mapping[str, str] | None,
        access_token: str | None,
    ) -> dict[str, str]:
        merged = {**client_headers, **(_normalize_headers(headers))}
        lower_keys = {k.lower(): k for k in merged}
        if access_token and "authorization" not in lower_keys:
            merged["Authorization"] = f"Bearer {access_token}"
        trace_key = HEADER_TRACE_ID.lower()
        if trace_key not in lower_keys or not merged.get(lower_keys.get(trace_key, HEADER_TRACE_ID)):
            merged[HEADER_TRACE_ID] = uuid.uuid4().hex
        return merged

    def _parse_success(self, payload: dict[str, Any], response_model: Any, trace_id: str | None) -> ApiResult[Any]:
        try:
            meta = ResponseMeta.model_validate(payload.get("meta") or {})
        except ValidationError as exc:
            raise SdkTransportError("Invalid response metadata", trace_id=trace_id, details=exc.errors()) from exc
        parsed_data = payload.get("data")
        if response_model is not None:
            try:
                parsed_data = _type_adapter(response_model).validate_python(_coerce_datetimes(parsed_data))
            except ValidationError as exc:
                raise SdkTransportError(
                    "Unable to parse response data", trace_id=meta.trace_id or trace_id, details=exc.errors()
                ) from exc
        return ApiResult(data=parsed_data, meta=meta, trace_id=meta.trace_id or trace_id)

    def _raise_error(self, payload: dict[str, Any], trace_id: str | None, status: int) -> None:
        error_body = payload.get("error") or {}
        meta_section = payload.get("meta") or {}
        if isinstance(meta_section, dict) and meta_section.get("trace_id"):
            trace_id = meta_section.get("trace_id")
        parsed_error = ErrorBody.model_validate(error_body) if isinstance(error_body, dict) else None
        code: ErrorCode | str = parsed_error.code if parsed_error else payload.get("code", ErrorCode.INTERNAL_ERROR)
        message = parsed_error.message if parsed_error else payload.get("message", "Request failed")
        details = parsed_error.details if parsed_error else error_body or payload
        raise SdkError(
            code=code, message=message, http_status=status, trace_id=trace_id, details=details, response=payload
        )

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        response_model: Any = None,
        access_token: str | None = None,
        use_webhooks: bool = False,
    ) -> ApiResult[Any]:
        if response_model is None:
            raise SdkTransportError("response_model is required for typed SDK requests")
        client = self._webhooks_client if use_webhooks else self._client
        prepared_headers = self._prepare_headers(
            client_headers=client.headers, headers=headers, access_token=access_token or self._access_token
        )
        try:
            response = await client.request(method, path, json=json, params=params, headers=prepared_headers)
        except httpx.RequestError as exc:
            raise SdkTransportError(f"Request failed: {exc}") from exc
        trace_id = response.headers.get(HEADER_TRACE_ID) or prepared_headers.get(HEADER_TRACE_ID)
        try:
            payload = response.json()
        except ValueError as exc:
            raise SdkTransportError(
                "Response was not valid JSON", trace_id=trace_id, http_status=response.status_code
            ) from exc
        ok_flag = payload.get("ok")
        if response.status_code >= 400 or ok_flag is False:
            self._raise_error(payload, trace_id, response.status_code)
        if ok_flag is not True:
            raise SdkTransportError(
                "Unexpected response envelope", trace_id=trace_id, http_status=response.status_code, details=payload
            )
        return self._parse_success(payload, response_model, trace_id)


class AuthApi(_ServiceBase):
    async def register(
        self,
        *,
        email: str,
        password: str,
        display_name: str | None = None,
        registration_code: str | None = None,
        referral_code: str | None = None,
        request: contracts.RegisterRequest | None = None,
    ) -> ApiResult[contracts.TokenPairResponse]:
        payload = self._payload(
            contracts.RegisterRequest,
            request,
            email=email,
            password=password,
            registration_code=registration_code,
            referral_code=referral_code,
        )
        if display_name:
            payload["display_name"] = display_name
        result = await self._client._request(
            "POST", f"{API_PREFIX}/auth/register", json=payload, response_model=contracts.TokenPairResponse
        )
        self._client.set_token_pair(result.data)
        return result

    async def login(
        self,
        *,
        email: str,
        password: str,
        totp_code: str | None = None,
        recovery_code: str | None = None,
        request: contracts.LoginRequest | None = None,
    ) -> ApiResult[contracts.TokenPairResponse]:
        payload = self._payload(
            contracts.LoginRequest,
            request,
            email=email,
            password=password,
            totp_code=totp_code,
            recovery_code=recovery_code,
        )
        result = await self._client._request(
            "POST", f"{API_PREFIX}/auth/login", json=payload, response_model=contracts.TokenPairResponse
        )
        self._client.set_token_pair(result.data)
        return result

    async def refresh(
        self, *, refresh_token: str | None = None, request: contracts.RefreshRequest | None = None
    ) -> ApiResult[contracts.TokenPairResponse]:
        token_value = refresh_token or self._client.refresh_token
        if not token_value:
            raise SdkTransportError("Refresh token is not set")
        payload = self._payload(contracts.RefreshRequest, request, refresh_token=token_value)
        result = await self._client._request(
            "POST", f"{API_PREFIX}/auth/refresh", json=payload, response_model=contracts.TokenPairResponse
        )
        self._client.set_token_pair(result.data)
        return result

    async def setup_2fa(self, *, user_id: str | None = None) -> ApiResult[TwoFactorSetupResult]:
        payload = self._payload(contracts.TwoFactorSetupRequest, None, user_id=user_id)
        return await self._client._request(
            "POST", f"{API_PREFIX}/auth/2fa/setup", json=payload, response_model=TwoFactorSetupResult
        )

    async def verify_2fa(
        self, *, user_id: str | None = None, code: str | None = None
    ) -> ApiResult[TwoFactorVerifyResult]:
        payload = self._payload(contracts.TwoFactorVerifyRequest, None, user_id=user_id, code=code)
        return await self._client._request(
            "POST", f"{API_PREFIX}/auth/2fa/verify", json=payload, response_model=TwoFactorVerifyResult
        )

    async def me(self) -> ApiResult[AuthMeResult]:
        return await self._client._request("GET", f"{API_PREFIX}/auth/me", response_model=AuthMeResult)

    async def list_sessions(
        self, request: contracts.UserSessionListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.UserSessionResponse]]:
        params = self._payload(contracts.UserSessionListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/auth/me/sessions",
            params=params or None,
            response_model=contracts.Page[contracts.UserSessionResponse],
        )

    async def rename_session(
        self,
        *,
        session_id: str,
        device_name: str,
        request: contracts.UserSessionUpdateRequest | None = None,
    ) -> ApiResult[contracts.UserSessionResponse]:
        payload = self._payload(contracts.UserSessionUpdateRequest, request, device_name=device_name)
        return await self._client._request(
            "PATCH",
            f"{API_PREFIX}/auth/me/sessions/{session_id}",
            json=payload,
            response_model=contracts.UserSessionResponse,
        )

    async def revoke_session(self, *, session_id: str) -> ApiResult[contracts.UserSessionRevokeResponse]:
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/auth/me/sessions/{session_id}/revoke",
            response_model=contracts.UserSessionRevokeResponse,
        )

    async def register_settings(self) -> ApiResult[dict]:
        return await self._client._request("GET", f"{API_PREFIX}/auth/register/settings", response_model=dict)

    async def logout(self) -> ApiResult[dict]:
        result = await self._client._request("POST", f"{API_PREFIX}/auth/logout", json={}, response_model=dict)
        self._client.set_access_token(None)
        self._client.set_refresh_token(None)
        return result

    async def update_me(self, *, display_name: str | None = None, **kwargs: Any) -> ApiResult[AuthMeResult]:
        payload: dict[str, Any] = {}
        if display_name is not None:
            payload["display_name"] = display_name
        payload.update({k: v for k, v in kwargs.items() if v is not None})
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/auth/me", json=payload, response_model=AuthMeResult
        )

    async def me_analytics(self) -> ApiResult[dict]:
        return await self._client._request("GET", f"{API_PREFIX}/auth/me/analytics", response_model=dict)

    async def me_storage(self) -> ApiResult[dict]:
        return await self._client._request("GET", f"{API_PREFIX}/auth/me/storage", response_model=dict)


class OrgsApi(_ServiceBase):
    async def list(
        self, request: contracts.OrgListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.OrgResponse]]:
        params = self._payload(contracts.OrgListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/orgs/", params=params or None, response_model=contracts.Page[contracts.OrgResponse]
        )

    async def get(self, *, org_id: str) -> ApiResult[contracts.OrgResponse]:
        return await self._client._request("GET", f"{API_PREFIX}/orgs/{org_id}", response_model=contracts.OrgResponse)

    async def overview(self, *, org_id: str) -> ApiResult[OrgOverviewResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/orgs/{org_id}/overview", response_model=OrgOverviewResponse
        )

    async def create(
        self, request: contracts.OrgCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.OrgResponse]:
        payload = self._payload(contracts.OrgCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/", json=payload, response_model=contracts.OrgResponse
        )

    async def invite_member(
        self, request: contracts.InviteRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.MembershipResponse]:
        payload = self._payload(contracts.InviteRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/members", json=payload, response_model=contracts.MembershipResponse
        )

    async def list_members(
        self, *, org_id: str, request: contracts.OrgMemberListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.MembershipResponse]]:
        params = self._payload(contracts.OrgMemberListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/orgs/{org_id}/members",
            params=params or None,
            response_model=contracts.Page[contracts.MembershipResponse],
        )

    async def list_invites(
        self, *, org_id: str, request: contracts.OrgMemberListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.MembershipResponse]]:
        params = self._payload(contracts.OrgMemberListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/orgs/{org_id}/invites",
            params=params or None,
            response_model=contracts.Page[contracts.MembershipResponse],
        )

    async def change_role(
        self, request: contracts.RoleChangeRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.MembershipResponse]:
        payload = self._payload(contracts.RoleChangeRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/members/role", json=payload, response_model=contracts.MembershipResponse
        )

    async def accept_invite(self, *, invite_id: str) -> ApiResult[contracts.MembershipResponse]:
        payload = {"invite_id": invite_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/invites/accept", json=payload, response_model=contracts.MembershipResponse
        )

    async def decline_invite(self, *, invite_id: str) -> ApiResult[contracts.MembershipResponse]:
        payload = {"invite_id": invite_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/invites/decline", json=payload, response_model=contracts.MembershipResponse
        )

    async def remove_member(
        self, *, org_id: str, user_id: str | None = None, member_id: str | None = None
    ) -> ApiResult[DeletionResult]:
        payload = self._payload(
            contracts.OrgMemberRemoveRequest, None, org_id=org_id, user_id=user_id, member_id=member_id
        )
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/members/remove", json=payload, response_model=DeletionResult
        )

    async def transfer(self, *, org_id: str, new_owner_user_id: str) -> ApiResult[contracts.OrgResponse]:
        payload = {"org_id": org_id, "new_owner_user_id": new_owner_user_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/transfer", json=payload, response_model=contracts.OrgResponse
        )

    async def quit(self, *, org_id: str) -> ApiResult[QuitResult]:
        payload = self._payload(contracts.OrgQuitRequest, None, org_id=org_id)
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/members/quit", json=payload, response_model=QuitResult
        )

    async def delete(
        self, request: contracts.OrgDeleteRequest | None = None, **kwargs: Any
    ) -> ApiResult[DeletionResult]:
        payload = self._payload(contracts.OrgDeleteRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/delete", json=payload, response_model=DeletionResult
        )

    async def bulk_update(self, *, updates: list[dict[str, Any]]) -> ApiResult[list[contracts.OrgResponse]]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/update", json={"updates": updates}, response_model=list[contracts.OrgResponse]
        )

    async def list_org_notifications(
        self, *, org_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.NotificationItem]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/orgs/{org_id}/notifications", params=params or None,
            response_model=contracts.Page[contracts.NotificationItem],
        )

    async def org_storage(self, *, org_id: str) -> ApiResult[dict]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/orgs/{org_id}/storage", response_model=dict
        )


class ModelsApi(_ServiceBase):
    async def detail(self, *, model_id: str) -> ApiResult[contracts.ModelResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/{model_id}", response_model=contracts.ModelResponse
        )

    async def create(
        self, request: contracts.ModelCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ModelResponse]:
        payload = self._payload(contracts.ModelCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/models/", json=payload, response_model=contracts.ModelResponse
        )

    async def list(
        self, request: contracts.ModelListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.ModelResponse]]:
        params = self._payload(contracts.ModelListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/models/",
            params=params or None,
            response_model=contracts.Page[contracts.ModelResponse],
        )

    async def delete(self, *, model_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request("DELETE", f"{API_PREFIX}/models/{model_id}", response_model=DeletionResult)

    async def upload_dataset_images(
        self, *, model_id: str, images: list[contracts.DatasetImagePayload]
    ) -> ApiResult[list[contracts.ModelDatasetImageResponse]]:
        payload = contracts.DatasetImageUploadRequest(images=images)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/models/{model_id}/dataset/images",
            json=payload.model_dump(exclude_none=True),
            response_model=list[contracts.ModelDatasetImageResponse],
        )

    async def generate_candidates_job(
        self, *, model_id: str, request: contracts.GenerateCandidatesRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ModelJobResponse]:
        payload = self._payload(contracts.GenerateCandidatesRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/models/{model_id}/jobs/generate-candidates",
            json=payload,
            response_model=contracts.ModelJobResponse,
        )

    async def list_model_jobs(self, *, model_id: str) -> ApiResult[list[contracts.ModelJobResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/{model_id}/jobs", response_model=list[contracts.ModelJobResponse]
        )

    async def get_model_job(self, *, job_id: str) -> ApiResult[contracts.ModelJobResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/model-jobs/{job_id}", response_model=contracts.ModelJobResponse
        )

    async def list_candidates(self, *, model_id: str) -> ApiResult[list[contracts.ModelCandidateResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/{model_id}/candidates", response_model=list[contracts.ModelCandidateResponse]
        )

    async def select_canonical(self, *, model_id: str, candidate_id: str) -> ApiResult[contracts.ModelResponse]:
        payload = self._payload(contracts.CanonicalSelectRequest, None, candidate_id=candidate_id)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/models/{model_id}/canonical",
            json=payload,
            response_model=contracts.ModelResponse,
        )

    async def generate_avatar_job(
        self, *, model_id: str, request: contracts.GenerateAvatarRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ModelJobResponse]:
        payload = self._payload(contracts.GenerateAvatarRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/models/{model_id}/jobs/generate-avatar",
            json=payload,
            response_model=contracts.ModelJobResponse,
        )

    async def list_generated_avatars(self, *, model_id: str) -> ApiResult[list[contracts.AvatarResponse]]:
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/models/{model_id}/generated-avatars",
            response_model=list[contracts.AvatarResponse],
        )

    async def get_generated_avatar(self, *, avatar_id: str) -> ApiResult[contracts.AvatarResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/avatars/{avatar_id}", response_model=contracts.AvatarResponse
        )

    async def list_avatars(
        self, *, model_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.AvatarProfileResponse]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/models/{model_id}/avatars",
            params=params or None,
            response_model=contracts.Page[contracts.AvatarProfileResponse],
        )

    async def get_avatar(self, *, avatar_id: str) -> ApiResult[contracts.AvatarProfileResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/avatar/{avatar_id}", response_model=contracts.AvatarProfileResponse
        )

    async def create_avatar(
        self, request: contracts.AvatarProfileCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.AvatarProfileResponse]:
        payload = self._payload(contracts.AvatarProfileCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/models/avatars", json=payload, response_model=contracts.AvatarProfileResponse
        )

    async def delete_avatar(self, *, avatar_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/models/avatar/{avatar_id}", response_model=DeletionResult
        )

    async def share(
        self, request: contracts.ModelShareRequest | None = None, **kwargs: Any
    ) -> ApiResult[ModelShareGrant]:
        payload = self._payload(contracts.ModelShareRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/models/share", json=payload, response_model=ModelShareGrant
        )

    async def list_shares(
        self, *, model_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[ModelShareGrant]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/models/{model_id}/shares",
            params=params or None,
            response_model=contracts.Page[ModelShareGrant],
        )

    async def update(
        self, request: contracts.ModelUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ModelResponse]:
        payload = self._payload(contracts.ModelUpdateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/models/update", json=payload, response_model=contracts.ModelResponse
        )

    async def fork(
        self, request: contracts.ModelForkRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ModelResponse]:
        payload = self._payload(contracts.ModelForkRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/models/fork", json=payload, response_model=contracts.ModelResponse
        )

    async def transfer(
        self, request: contracts.ModelTransferRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ModelResponse]:
        payload = self._payload(contracts.ModelTransferRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/models/transfer", json=payload, response_model=contracts.ModelResponse
        )

    async def character_schema(self) -> ApiResult[contracts.CharacterPromptSchemaResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/character-designer/schema",
            response_model=contracts.CharacterPromptSchemaResponse,
        )

    async def create_character_creation(
        self, request: contracts.CharacterCreationRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CharacterCreationEnqueueResponse]:
        payload = self._payload(contracts.CharacterCreationRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/models/character-creations", json=payload,
            response_model=contracts.CharacterCreationEnqueueResponse,
        )

    async def list_character_creations(
        self, request: contracts.CharacterCreationListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.CharacterCreationResponse]]:
        params = self._payload(contracts.CharacterCreationListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/character-creations", params=params or None,
            response_model=contracts.Page[contracts.CharacterCreationResponse],
        )

    async def get_character_creation(self, *, creation_id: str) -> ApiResult[contracts.CharacterCreationResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/character-creations/{creation_id}",
            response_model=contracts.CharacterCreationResponse,
        )

    async def patch_character_creation(
        self, *, creation_id: str, request: contracts.CharacterCreationUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CharacterCreationResponse]:
        payload = self._payload(contracts.CharacterCreationUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/models/character-creations/{creation_id}", json=payload,
            response_model=contracts.CharacterCreationResponse,
        )

    async def revoke_share(self, *, grant_id: str) -> ApiResult[RevokedResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/models/revoke", json={"grant_id": grant_id},
            response_model=RevokedResult,
        )

    async def model_replies(
        self, *, model_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[dict]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/models/{model_id}/replies", params=params or None,
            response_model=contracts.Page[dict],
        )


class PromptsApi(_ServiceBase):
    async def list_templates(
        self, request: contracts.PromptTemplateListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.PromptTemplateResponse]]:
        params = self._payload(contracts.PromptTemplateListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/prompts/templates",
            params=params or None,
            response_model=contracts.Page[contracts.PromptTemplateResponse],
        )

    async def get_template(self, *, template_id: str) -> ApiResult[contracts.PromptTemplateResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/prompts/template/{template_id}", response_model=contracts.PromptTemplateResponse
        )

    async def update_template(
        self, request: contracts.PromptTemplateUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PromptTemplateResponse]:
        payload = self._payload(contracts.PromptTemplateUpdateRequest, request, **kwargs)
        template_id = payload.pop("template_id")
        return await self._client._request(
            "PATCH",
            f"{API_PREFIX}/prompts/template/{template_id}",
            json=payload,
            response_model=contracts.PromptTemplateResponse,
        )

    async def set_template_examples(
        self,
        *,
        template_id: str,
        request: contracts.PromptTemplateExamplesUpdateRequest | None = None,
        **kwargs: Any,
    ) -> ApiResult[contracts.PromptTemplateResponse]:
        payload = self._payload(contracts.PromptTemplateExamplesUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PUT",
            f"{API_PREFIX}/prompts/template/{template_id}/examples",
            json=payload,
            response_model=contracts.PromptTemplateResponse,
        )

    async def lock_template(self, *, template_id: str) -> ApiResult[contracts.PromptTemplateResponse]:
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/prompts/template/{template_id}/lock",
            response_model=contracts.PromptTemplateResponse,
        )

    async def unlock_template(self, *, template_id: str) -> ApiResult[contracts.PromptTemplateResponse]:
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/prompts/template/{template_id}/unlock",
            response_model=contracts.PromptTemplateResponse,
        )

    async def duplicate_template(
        self, request: contracts.PromptTemplateDuplicateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PromptTemplateResponse]:
        payload = self._payload(contracts.PromptTemplateDuplicateRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/prompts/template/duplicate",
            json=payload,
            response_model=contracts.PromptTemplateResponse,
        )

    async def list_versions(
        self, *, template_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.PromptVersionResponse]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/prompts/template/{template_id}/versions",
            params=params or None,
            response_model=contracts.Page[contracts.PromptVersionResponse],
        )

    async def get_version(self, *, version_id: str) -> ApiResult[contracts.PromptVersionResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/prompts/version/{version_id}", response_model=contracts.PromptVersionResponse
        )

    async def list_runs(
        self, request: contracts.PromptRunListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.PromptRunResponse]]:
        params = self._payload(contracts.PromptRunListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/prompts/runs",
            params=params or None,
            response_model=contracts.Page[contracts.PromptRunResponse],
        )

    async def model_runs(
        self, *, model_id: str, request: contracts.PromptRunListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.PromptRunResponse]]:
        params = self._payload(contracts.PromptRunListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/prompts/models/{model_id}/runs",
            params=params or None,
            response_model=contracts.Page[contracts.PromptRunResponse],
        )

    async def create_template(
        self, request: contracts.PromptTemplateCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PromptTemplateResponse]:
        payload = self._payload(contracts.PromptTemplateCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/prompts/", json=payload, response_model=contracts.PromptTemplateResponse
        )

    async def create_version(
        self, request: contracts.PromptVersionCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PromptVersionResponse]:
        payload = self._payload(contracts.PromptVersionCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/prompts/version", json=payload, response_model=contracts.PromptVersionResponse
        )

    async def link_template(
        self, request: contracts.PromptTemplateModelLinkRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PromptTemplateModelLinkResponse]:
        payload = self._payload(contracts.PromptTemplateModelLinkRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/prompts/link", json=payload, response_model=contracts.PromptTemplateModelLinkResponse
        )

    async def run(
        self, request: contracts.PromptRunCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PromptRunBundleResponse]:
        payload = self._payload(contracts.PromptRunCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/prompts/run", json=payload, response_model=contracts.PromptRunBundleResponse
        )

    async def delete_template(self, *, template_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/prompts/template/{template_id}", response_model=DeletionResult
        )

    async def update_version_config(self, *, version_id: str, **kwargs: Any) -> ApiResult[contracts.PromptVersionResponse]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/prompts/version/update", json={"version_id": version_id, **kwargs},
            response_model=contracts.PromptVersionResponse,
        )

    async def unlink_template(self, *, template_id: str, model_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/prompts/unlink", json={"template_id": template_id, "model_id": model_id},
            response_model=DeletionResult,
        )

    async def delete_run(self, *, run_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/prompts/run/delete", json={"run_id": run_id}, response_model=DeletionResult
        )


class JobsApi(_ServiceBase):
    async def list(
        self, request: contracts.JobListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.JobResponse]]:
        params = self._payload(contracts.JobListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/jobs/", params=params or None, response_model=contracts.Page[contracts.JobResponse]
        )

    async def get(self, *, job_id: str) -> ApiResult[contracts.JobResponse]:
        return await self._client._request("GET", f"{API_PREFIX}/jobs/{job_id}", response_model=contracts.JobResponse)

    async def retry(self, *, job_id: str) -> ApiResult[contracts.JobResponse]:
        payload = {"job_id": job_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/jobs/retry", json=payload, response_model=contracts.JobResponse
        )

    async def history(self, *, job_id: str) -> ApiResult[list[contracts.JobStatusHistoryResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/jobs/history/{job_id}", response_model=list[contracts.JobStatusHistoryResponse]
        )

    async def outputs(self, *, job_id: str) -> ApiResult[list[contracts.AssetPublicResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/jobs/{job_id}/outputs", response_model=list[contracts.AssetPublicResponse]
        )

    async def output_thumbnails(
        self,
        *,
        job_ids: list[str],
    ) -> ApiResult[dict[str, contracts.AssetPublicResponse]]:
        payload = {"job_ids": job_ids}
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/jobs/outputs/thumbnails",
            json=payload,
            response_model=dict[str, contracts.AssetPublicResponse],
        )

    async def pipeline(self, *, pipeline_id: str) -> ApiResult[contracts.PipelineResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/jobs/pipelines/{pipeline_id}", response_model=contracts.PipelineResponse
        )

    async def save_output_asset(self, *, job_id: str, asset_id: str) -> ApiResult[AssetPublicResponse]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/jobs/{job_id}/outputs/{asset_id}/save", json={},
            response_model=AssetPublicResponse,
        )


class DownloadsApi(_ServiceBase):
    async def create(
        self, request: contracts.ContentDownloadCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ContentDownloadResponse]:
        payload = self._payload(contracts.ContentDownloadCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/downloads/",
            json=payload,
            response_model=contracts.ContentDownloadResponse,
        )

    async def batch_create(
        self, request: contracts.ContentDownloadBatchCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ContentDownloadBatchCreateResult]:
        payload = self._payload(contracts.ContentDownloadBatchCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/downloads/batch",
            json=payload,
            response_model=contracts.ContentDownloadBatchCreateResult,
        )

    async def list(
        self, request: contracts.ContentDownloadListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.ContentDownloadResponse]]:
        params = self._payload(contracts.ContentDownloadListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/downloads/",
            params=params or None,
            response_model=contracts.Page[contracts.ContentDownloadResponse],
        )

    async def get(self, *, download_id: str) -> ApiResult[contracts.ContentDownloadResponse]:
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/downloads/{download_id}",
            response_model=contracts.ContentDownloadResponse,
        )

    async def outputs(self, *, download_id: str) -> ApiResult[list[contracts.ContentDownloadOutputResponse]]:
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/downloads/{download_id}/outputs",
            response_model=list[contracts.ContentDownloadOutputResponse],
        )

    async def cancel(self, *, download_id: str) -> ApiResult[contracts.ContentDownloadResponse]:
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/downloads/cancel",
            json={"download_id": download_id},
            response_model=contracts.ContentDownloadResponse,
        )

    async def retry(self, *, download_id: str) -> ApiResult[contracts.ContentDownloadResponse]:
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/downloads/retry",
            json={"download_id": download_id},
            response_model=contracts.ContentDownloadResponse,
        )

    async def delete(self, *, download_id: str) -> ApiResult[DeletionResult]:
        payload = self._payload(contracts.ContentDownloadDeleteRequest, None, download_id=download_id)
        return await self._client._request(
            "POST", f"{API_PREFIX}/downloads/delete", json=payload, response_model=DeletionResult
        )


class CreditsApi(_ServiceBase):
    async def wallet(self) -> ApiResult[contracts.UserWallet]:
        return await self._client._request("GET", f"{API_PREFIX}/wallet", response_model=contracts.UserWallet)

    async def usage(
        self, request: contracts.UsageListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.UsageRecord]]:
        params = self._payload(contracts.UsageListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/usage", params=params or None, response_model=contracts.Page[contracts.UsageRecord]
        )

    async def rate_cards(self) -> ApiResult[list[contracts.RateCardEntry]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/rate-cards", response_model=list[contracts.RateCardEntry]
        )

    async def usage_series(self, request: contracts.UsageListQuery | None = None, **kwargs: Any) -> ApiResult[dict]:
        params = self._payload(contracts.UsageListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/credits/usage/series", params=params or None, response_model=dict
        )


class BillingApi(_ServiceBase):
    async def products(self) -> ApiResult[list[contracts.BillingProduct]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/billing/products", response_model=list[contracts.BillingProduct]
        )

    async def summary(self) -> ApiResult[contracts.BillingSummary]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/billing/summary", response_model=contracts.BillingSummary
        )

    async def checkout_topup(
        self, request: contracts.BillingCheckoutCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.BillingCheckoutCreateResult]:
        payload = self._payload(contracts.BillingCheckoutCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/billing/checkout/topup",
            json=payload,
            response_model=contracts.BillingCheckoutCreateResult,
        )

    async def checkout_subscription(
        self, request: contracts.BillingCheckoutCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.BillingCheckoutCreateResult]:
        payload = self._payload(contracts.BillingCheckoutCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/billing/checkout/subscription",
            json=payload,
            response_model=contracts.BillingCheckoutCreateResult,
        )

    async def portal(
        self, request: contracts.BillingPortalCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.BillingPortalCreateResult]:
        payload = self._payload(contracts.BillingPortalCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/billing/portal",
            json=payload,
            response_model=contracts.BillingPortalCreateResult,
        )

    async def change_subscription(
        self, request: contracts.BillingSubscriptionChangeRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.BillingSubscriptionChangeResult]:
        payload = self._payload(contracts.BillingSubscriptionChangeRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/billing/subscription/change",
            json=payload,
            response_model=contracts.BillingSubscriptionChangeResult,
        )


class AdminDownloadsApi(_ServiceBase):
    async def list_provider_settings(self) -> ApiResult[list[contracts.AdminDownloadProviderSettingResponse]]:
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/admin/downloads/providers",
            response_model=list[contracts.AdminDownloadProviderSettingResponse],
        )

    async def update_provider_setting(
        self,
        *,
        platform: str,
        request: contracts.AdminDownloadProviderSettingUpdateRequest | None = None,
        **kwargs: Any,
    ) -> ApiResult[contracts.AdminDownloadProviderSettingResponse]:
        payload = self._payload(contracts.AdminDownloadProviderSettingUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PUT",
            f"{API_PREFIX}/admin/downloads/providers/{platform}",
            json=payload,
            response_model=contracts.AdminDownloadProviderSettingResponse,
        )


class PoolingApi(_ServiceBase):
    async def model_pool(self, *, model_id: str) -> ApiResult[contracts.PoolView]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/pooling/model/{model_id}", response_model=contracts.PoolView
        )

    async def invites(
        self, request: contracts.PoolingInviteListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.PoolingInvite]]:
        params = self._payload(contracts.PoolingInviteListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/pooling/invites",
            params=params or None,
            response_model=contracts.Page[contracts.PoolingInvite],
        )

    async def propose(self, *, model_id: str, members: list[dict]) -> ApiResult[contracts.ModelPool]:
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/pooling/propose",
            json={"model_id": model_id, "members": members},
            response_model=contracts.ModelPool,
        )

    async def accept(self, *, member_id: str) -> ApiResult[AcceptedResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/pooling/accept", json={"member_id": member_id}, response_model=AcceptedResult
        )

    async def decline(self, *, member_id: str) -> ApiResult[DeclinedResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/pooling/decline", json={"member_id": member_id}, response_model=DeclinedResult
        )

    async def revoke(self, *, pool_id: str) -> ApiResult[RevokedResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/pooling/revoke", json={"pool_id": pool_id}, response_model=RevokedResult
        )


class AnalyticsApi(_ServiceBase):
    async def revenue(self, *, model_id: str | None = None) -> ApiResult[RevenueSummary]:
        params = {"model_id": model_id} if model_id else None
        return await self._client._request(
            "GET", f"{API_PREFIX}/analytics/revenue", params=params, response_model=RevenueSummary
        )

    async def org_revenue(self, *, org_id: str) -> ApiResult[RevenueSummary]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/analytics/revenue/org/{org_id}", response_model=RevenueSummary
        )


class AuditApi(_ServiceBase):
    async def me(self) -> ApiResult[list[contracts.AuditLog]]:
        return await self._client._request("GET", f"{API_PREFIX}/audit/me", response_model=list[contracts.AuditLog])

    async def org(self, *, org_id: str) -> ApiResult[list[contracts.AuditLog]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/audit/org/{org_id}", response_model=list[contracts.AuditLog]
        )


class SystemApi(_ServiceBase):
    async def health(self) -> ApiResult[contracts.SystemHealthSummary]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/system/health", response_model=contracts.SystemHealthSummary
        )

    async def version(self) -> ApiResult[contracts.SystemVersionResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/system/version", response_model=contracts.SystemVersionResponse
        )

    async def enums(self) -> ApiResult[contracts.SystemEnumsResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/system/enums", response_model=contracts.SystemEnumsResponse
        )


class NotificationsApi(_ServiceBase):
    async def create(
        self, *, org_id: str, model_id: str | None = None, title: str, body: str
    ) -> ApiResult[contracts.InternalNotification]:
        payload = {"org_id": org_id, "model_id": model_id, "title": title, "body": body}
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/notifications/",
            json=payload,
            response_model=contracts.InternalNotification,
        )

    async def delete(self, *, notification_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/notifications/{notification_id}", response_model=DeletionResult
        )

    async def list(self) -> ApiResult[list[NotificationItem]]:
        return await self._client._request("GET", f"{API_PREFIX}/notifications/", response_model=list[NotificationItem])

    async def mark_read(self, *, notification_id: str) -> ApiResult[ReadResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/notifications/{notification_id}/read", response_model=ReadResult
        )

    async def mark_unread(self, *, notification_id: str) -> ApiResult[UnreadResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/notifications/{notification_id}/unread", response_model=UnreadResult
        )

    async def mute(self, *, notification_id: str) -> ApiResult[MutedResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/notifications/{notification_id}/mute", response_model=MutedResult
        )

    async def unmute(self, *, notification_id: str) -> ApiResult[UnmutedResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/notifications/{notification_id}/unmute", response_model=UnmutedResult
        )


class AssetsApi(_ServiceBase):
    async def create(
        self, request: contracts.AssetCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[AssetPublicResponse]:
        payload = self._payload(contracts.AssetCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/", json=payload, response_model=AssetPublicResponse
        )

    async def delete(self, *, asset_id: str) -> ApiResult[DeletionResult]:
        payload = {"asset_id": asset_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/delete", json=payload, response_model=DeletionResult
        )

    async def get(self, *, asset_id: str) -> ApiResult[AssetPublicResponse]:
        return await self._client._request("GET", f"{API_PREFIX}/assets/{asset_id}", response_model=AssetPublicResponse)

    async def update(
        self, *, asset_id: str, request: contracts.AssetUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[AssetPublicResponse]:
        payload = self._payload(contracts.AssetUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/assets/{asset_id}", json=payload or {}, response_model=AssetPublicResponse
        )

    async def link(
        self, request: contracts.AssetLinkRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.AssetLinkResponse]:
        payload = self._payload(contracts.AssetLinkRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/link", json=payload, response_model=contracts.AssetLinkResponse
        )

    async def unlink(self, *, asset_id: str, model_id: str) -> ApiResult[DeletionResult]:
        payload = {"asset_id": asset_id, "model_id": model_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/unlink", json=payload, response_model=DeletionResult
        )

    async def archive(self, *, asset_id: str) -> ApiResult[AssetPublicResponse]:
        payload = {"asset_id": asset_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/archive", json=payload, response_model=AssetPublicResponse
        )

    async def permadelete(self, *, asset_id: str) -> ApiResult[DeletionResult]:
        payload = {"asset_id": asset_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/permadelete", json=payload, response_model=DeletionResult
        )

    async def list(
        self, request: contracts.AssetListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[AssetPublicResponse]]:
        params = self._payload(contracts.AssetListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/assets/",
            params=params or None,
            response_model=contracts.Page[AssetPublicResponse],
        )

    async def model_assets(
        self, *, model_id: str, request: contracts.AssetListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[AssetPublicResponse]]:
        params = self._payload(contracts.AssetListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/assets/models/{model_id}",
            params=params or None,
            response_model=contracts.Page[AssetPublicResponse],
        )

    async def upload_url(self, **kwargs: Any) -> ApiResult[dict]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/upload", json=kwargs, response_model=dict
        )

    async def retry_upload(self, *, asset_id: str) -> ApiResult[dict]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/upload/retry", json={"asset_id": asset_id}, response_model=dict
        )

    async def get_url(self, *, asset_id: str) -> ApiResult[dict]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/assets/{asset_id}/url", response_model=dict
        )

    async def get_content(self, *, asset_id: str) -> ApiResult[dict]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/assets/{asset_id}/content", response_model=dict
        )

    async def download(self, *, asset_id: str) -> ApiResult[dict]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/assets/{asset_id}/download", response_model=dict
        )

    async def bulk_update(self, request: contracts.AssetBulkUpdateRequest | None = None, **kwargs: Any) -> ApiResult[dict]:
        payload = self._payload(contracts.AssetBulkUpdateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/bulk-update", json=payload, response_model=dict
        )

    async def mark_delete(self, *, asset_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/assets/delete", json={"asset_id": asset_id}, response_model=DeletionResult
        )


class CollectionsApi(_ServiceBase):
    async def create(
        self, request: contracts.CollectionCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CollectionResponse]:
        payload = self._payload(contracts.CollectionCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/collections/", json=payload, response_model=contracts.CollectionResponse
        )

    async def list(
        self, request: contracts.CollectionListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.CollectionResponse]]:
        params = self._payload(contracts.CollectionListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/collections/",
            params=params or None,
            response_model=contracts.Page[contracts.CollectionResponse],
        )

    async def get(
        self, *, collection_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CollectionDetailResponse]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/collections/{collection_id}",
            params=params or None,
            response_model=contracts.CollectionDetailResponse,
        )

    async def list_items(
        self, *, collection_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.CollectionItemResponse]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/collections/{collection_id}/items",
            params=params or None,
            response_model=contracts.Page[contracts.CollectionItemResponse],
        )

    async def update(
        self, *, collection_id: str, request: contracts.CollectionUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CollectionResponse]:
        payload = self._payload(contracts.CollectionUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH",
            f"{API_PREFIX}/collections/{collection_id}",
            json=payload or {},
            response_model=contracts.CollectionResponse,
        )

    async def delete(self, *, collection_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/collections/{collection_id}", response_model=DeletionResult
        )

    async def add_item(
        self, request: contracts.CollectionItemCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CollectionItemResponse]:
        payload = self._payload(contracts.CollectionItemCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/collections/items", json=payload, response_model=contracts.CollectionItemResponse
        )

    async def update_item(
        self, *, item_id: str, request: contracts.CollectionItemUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CollectionItemResponse]:
        payload = self._payload(contracts.CollectionItemUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH",
            f"{API_PREFIX}/collections/items/{item_id}",
            json=payload or {},
            response_model=contracts.CollectionItemResponse,
        )

    async def remove_item(self, *, item_id: str) -> ApiResult[DeletionResult]:
        payload = {"item_id": item_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/collections/items/remove", json=payload, response_model=DeletionResult
        )

    async def link(
        self, request: contracts.CollectionLinkRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CollectionLinkResponse]:
        payload = self._payload(contracts.CollectionLinkRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/collections/link", json=payload, response_model=contracts.CollectionLinkResponse
        )

    async def unlink(self, *, collection_id: str, model_id: str) -> ApiResult[DeletionResult]:
        payload = {"collection_id": collection_id, "model_id": model_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/collections/unlink", json=payload, response_model=DeletionResult
        )

    async def share(
        self, request: contracts.CollectionShareRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ModelShareGrant]:
        payload = self._payload(contracts.CollectionShareRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/collections/share", json=payload, response_model=contracts.ModelShareGrant
        )

    async def revoke(self, *, grant_id: str) -> ApiResult[RevokedResult]:
        payload = {"grant_id": grant_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/collections/revoke", json=payload, response_model=RevokedResult
        )

    async def shares(
        self, *, collection_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.ModelShareGrant]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/collections/{collection_id}/shares",
            params=params or None,
            response_model=contracts.Page[contracts.ModelShareGrant],
        )


class PostsApi(_ServiceBase):
    async def get_policy(self, *, org_id: str | None = None) -> ApiResult[contracts.PostingPolicyResponse]:
        params = {"org_id": org_id} if org_id else None
        return await self._client._request(
            "GET", f"{API_PREFIX}/posts/policy", params=params, response_model=contracts.PostingPolicyResponse
        )

    async def set_policy(
        self, request: contracts.PostingPolicyRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PostingPolicyResponse]:
        payload = self._payload(contracts.PostingPolicyRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/posts/policy", json=payload, response_model=contracts.PostingPolicyResponse
        )

    async def create(
        self, request: contracts.PostCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PostResponse]:
        payload = self._payload(contracts.PostCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/posts/", json=payload, response_model=contracts.PostResponse
        )

    async def approve(
        self, request: contracts.ApproveRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PostResponse]:
        payload = self._payload(contracts.ApproveRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/posts/approve", json=payload, response_model=contracts.PostResponse
        )

    async def publish(
        self, request: contracts.PublishRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PostResponse]:
        payload = self._payload(contracts.PublishRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/posts/publish", json=payload, response_model=contracts.PostResponse
        )


class ScheduleApi(_ServiceBase):
    async def catalog(self) -> ApiResult[contracts.ScheduleCatalogResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/schedule/catalog", response_model=contracts.ScheduleCatalogResponse
        )

    async def list(
        self, request: contracts.ScheduleListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.ScheduleEntryResponse]]:
        params = self._payload(contracts.ScheduleListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/schedule/",
            params=params or None,
            response_model=contracts.Page[contracts.ScheduleEntryResponse],
        )

    async def create(
        self, request: contracts.ScheduleEntryCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ScheduleEntryResponse]:
        payload = self._payload(contracts.ScheduleEntryCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/schedule/", json=payload, response_model=contracts.ScheduleEntryResponse
        )

    async def update(
        self, *, schedule_id: str, request: contracts.ScheduleEntryUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ScheduleEntryResponse]:
        payload = self._payload(contracts.ScheduleEntryUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH",
            f"{API_PREFIX}/schedule/{schedule_id}",
            json=payload,
            response_model=contracts.ScheduleEntryResponse,
        )

    async def complete(
        self, request: contracts.ScheduleCompleteRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ScheduleEntryResponse]:
        payload = self._payload(contracts.ScheduleCompleteRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/schedule/complete",
            json=payload,
            response_model=contracts.ScheduleEntryResponse,
        )

    async def delete(self, *, schedule_id: str) -> ApiResult[contracts.DeletionResult]:
        return await self._client._request(
            "DELETE",
            f"{API_PREFIX}/schedule/{schedule_id}",
            response_model=contracts.DeletionResult,
        )

    async def list_recurring_rules(
        self, request: contracts.RecurringRuleListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.RecurringRuleResponse]]:
        params = self._payload(contracts.RecurringRuleListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/schedule/recurring-rules", params=params or None,
            response_model=contracts.Page[contracts.RecurringRuleResponse],
        )

    async def create_recurring_rule(
        self, request: contracts.RecurringRuleCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.RecurringRuleResponse]:
        payload = self._payload(contracts.RecurringRuleCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/schedule/recurring-rules", json=payload,
            response_model=contracts.RecurringRuleResponse,
        )

    async def update_recurring_rule(
        self, *, rule_id: str, request: contracts.RecurringRuleUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.RecurringRuleResponse]:
        payload = self._payload(contracts.RecurringRuleUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/schedule/recurring-rules/{rule_id}", json=payload,
            response_model=contracts.RecurringRuleResponse,
        )

    async def delete_recurring_rule(self, *, rule_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/schedule/recurring-rules/{rule_id}", response_model=DeletionResult
        )

    async def toggle_rule(self, *, rule_id: str) -> ApiResult[contracts.RecurringRuleResponse]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/schedule/recurring-rules/{rule_id}/toggle", json={},
            response_model=contracts.RecurringRuleResponse,
        )


class CalendarFeedsApi(_ServiceBase):
    async def list(self) -> ApiResult[list[contracts.CalendarSubscriptionResponse]]:
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/calendar-feeds/",
            response_model=list[contracts.CalendarSubscriptionResponse],
        )

    async def create(
        self, request: contracts.CalendarSubscriptionCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CalendarSubscriptionResponse]:
        payload = self._payload(contracts.CalendarSubscriptionCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/calendar-feeds/",
            json=payload,
            response_model=contracts.CalendarSubscriptionResponse,
        )

    async def update(
        self,
        *,
        subscription_id: str,
        request: contracts.CalendarSubscriptionUpdateRequest | None = None,
        **kwargs: Any,
    ) -> ApiResult[contracts.CalendarSubscriptionResponse]:
        payload = self._payload(contracts.CalendarSubscriptionUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH",
            f"{API_PREFIX}/calendar-feeds/{subscription_id}",
            json=payload,
            response_model=contracts.CalendarSubscriptionResponse,
        )

    async def delete(self, *, subscription_id: str) -> ApiResult[contracts.DeletionResult]:
        return await self._client._request(
            "DELETE",
            f"{API_PREFIX}/calendar-feeds/{subscription_id}",
            response_model=contracts.DeletionResult,
        )

    async def regenerate_token(self, *, subscription_id: str) -> ApiResult[contracts.CalendarSubscriptionResponse]:
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/calendar-feeds/{subscription_id}/regenerate-token",
            response_model=contracts.CalendarSubscriptionResponse,
        )


class InternalApi(_ServiceBase):
    async def register_worker(
        self, request: contracts.WorkerRegisterRequest | None = None, admin_token: str | None = None, **kwargs: Any
    ) -> ApiResult[contracts.WorkerRegisterResponse]:
        payload = self._payload(contracts.WorkerRegisterRequest, request, **kwargs)
        headers = {HEADER_ADMIN_TOKEN: admin_token} if admin_token else None
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/workers/register",
            json=payload,
            headers=headers,
            response_model=contracts.WorkerRegisterResponse,
        )

    async def worker_token(
        self, request: contracts.WorkerTokenRequest | None = None, bootstrap: str | None = None, **kwargs: Any
    ) -> ApiResult[contracts.WorkerTokenResponse]:
        payload = self._payload(contracts.WorkerTokenRequest, request, **kwargs)
        headers = {HEADER_WORKER_BOOTSTRAP: bootstrap} if bootstrap else None
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/workers/token",
            json=payload,
            headers=headers,
            response_model=contracts.WorkerTokenResponse,
        )

    async def get_job(self, *, job_id: str, access_token: str | None = None) -> ApiResult[contracts.JobResponse]:
        return await self._client._request(
            "GET",
            f"{INTERNAL_PREFIX}/jobs/{job_id}",
            response_model=contracts.JobResponse,
            access_token=access_token,
        )

    async def claim_job(self, *, job_id: str, access_token: str | None = None) -> ApiResult[contracts.JobClaimResponse]:
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/jobs/{job_id}/claim",
            response_model=contracts.JobClaimResponse,
            access_token=access_token,
        )

    async def reclaim_job(self, *, job_id: str, access_token: str | None = None) -> ApiResult[contracts.JobClaimResponse]:
        """Reclaim a running job whose previous worker died (running + unclaimed)."""
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/jobs/{job_id}/reclaim",
            response_model=contracts.JobClaimResponse,
            access_token=access_token,
        )

    async def force_claim_job(self, *, job_id: str, access_token: str | None = None) -> ApiResult[contracts.JobClaimResponse]:
        """Force-claim a non-terminal job regardless of status or existing claim."""
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/jobs/{job_id}/force-claim",
            response_model=contracts.JobClaimResponse,
            access_token=access_token,
        )

    async def worker_status(
        self,
        *,
        request: contracts.WorkerStatusRequest | None = None,
        access_token: str | None = None,
        **kwargs: Any,
    ) -> ApiResult[dict]:
        payload = self._payload(contracts.WorkerStatusRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/workers/me/status",
            json=payload,
            response_model=dict,
            access_token=access_token,
        )

    async def list_stale_running_jobs(
        self,
        *,
        older_than_minutes: int = 30,
        admin_token: str | None = None,
    ) -> ApiResult[list[contracts.JobResponse]]:
        headers = {HEADER_ADMIN_TOKEN: admin_token} if admin_token else None
        return await self._client._request(
            "GET",
            f"{INTERNAL_PREFIX}/jobs/recovery/stale-running",
            params={"older_than_minutes": older_than_minutes},
            headers=headers,
            response_model=list[contracts.JobResponse],
        )

    async def release_dead_worker_claims(
        self,
        *,
        request: contracts.ReleaseDeadClaimsRequest | None = None,
        admin_token: str | None = None,
        **kwargs: Any,
    ) -> ApiResult[contracts.ReleaseDeadClaimsResponse]:
        payload = self._payload(contracts.ReleaseDeadClaimsRequest, request, **kwargs)
        headers = {HEADER_ADMIN_TOKEN: admin_token} if admin_token else None
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/jobs/recovery/release-dead-claims",
            json=payload,
            headers=headers,
            response_model=contracts.ReleaseDeadClaimsResponse,
        )

    async def get_download(
        self,
        *,
        download_id: str,
        access_token: str | None = None,
    ) -> ApiResult[contracts.ContentDownloadResponse]:
        return await self._client._request(
            "GET",
            f"{INTERNAL_PREFIX}/downloads/{download_id}",
            response_model=contracts.ContentDownloadResponse,
            access_token=access_token,
        )

    async def claim_download(
        self,
        *,
        download_id: str,
        access_token: str | None = None,
    ) -> ApiResult[contracts.ContentDownloadClaimResponse]:
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/downloads/{download_id}/claim",
            response_model=contracts.ContentDownloadClaimResponse,
            access_token=access_token,
        )

    async def reclaim_download(
        self,
        *,
        download_id: str,
        access_token: str | None = None,
    ) -> ApiResult[contracts.ContentDownloadClaimResponse]:
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/downloads/{download_id}/reclaim",
            response_model=contracts.ContentDownloadClaimResponse,
            access_token=access_token,
        )

    async def download_heartbeat(
        self,
        *,
        download_id: str,
        access_token: str | None = None,
    ) -> ApiResult[contracts.ContentDownloadResponse]:
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/downloads/{download_id}/heartbeat",
            response_model=contracts.ContentDownloadResponse,
            access_token=access_token,
        )

    async def download_progress(
        self,
        *,
        download_id: str,
        request: contracts.ContentDownloadProgressRequest | None = None,
        access_token: str | None = None,
        **kwargs: Any,
    ) -> ApiResult[contracts.ContentDownloadResponse]:
        payload = self._payload(contracts.ContentDownloadProgressRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/downloads/{download_id}/progress",
            json=payload,
            response_model=contracts.ContentDownloadResponse,
            access_token=access_token,
        )

    async def complete_download(
        self,
        *,
        download_id: str,
        request: contracts.ContentDownloadCompleteRequest | None = None,
        access_token: str | None = None,
        **kwargs: Any,
    ) -> ApiResult[contracts.ContentDownloadCompletionResult]:
        payload = self._payload(contracts.ContentDownloadCompleteRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/downloads/{download_id}/complete",
            json=payload,
            response_model=contracts.ContentDownloadCompletionResult,
            access_token=access_token,
        )

    async def fail_download(
        self,
        *,
        download_id: str,
        request: contracts.ContentDownloadFailRequest | None = None,
        access_token: str | None = None,
        **kwargs: Any,
    ) -> ApiResult[contracts.ContentDownloadResponse]:
        payload = self._payload(contracts.ContentDownloadFailRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/downloads/{download_id}/fail",
            json=payload,
            response_model=contracts.ContentDownloadResponse,
            access_token=access_token,
        )

    async def heartbeat(self, *, job_id: str, access_token: str | None = None) -> ApiResult[contracts.JobResponse]:
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/jobs/{job_id}/heartbeat",
            response_model=contracts.JobResponse,
            access_token=access_token,
        )

    async def progress(
        self,
        *,
        job_id: str,
        request: contracts.JobProgressRequest | None = None,
        access_token: str | None = None,
        **kwargs: Any,
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.JobProgressRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/jobs/{job_id}/progress",
            json=payload,
            response_model=contracts.JobResponse,
            access_token=access_token,
        )

    async def complete(
        self,
        *,
        job_id: str,
        request: contracts.JobCompleteRequest | None = None,
        access_token: str | None = None,
        **kwargs: Any,
    ) -> ApiResult[JobCompletionResult]:
        payload = self._payload(contracts.JobCompleteRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/jobs/{job_id}/complete",
            json=payload,
            response_model=JobCompletionResult,
            access_token=access_token,
        )

    async def fail(
        self,
        *,
        job_id: str,
        request: contracts.JobFailRequest | None = None,
        access_token: str | None = None,
        **kwargs: Any,
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.JobFailRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{INTERNAL_PREFIX}/jobs/{job_id}/fail",
            json=payload,
            response_model=contracts.JobResponse,
            access_token=access_token,
        )



class ThreadsApi(_ServiceBase):
    async def connect_callback(self, *, code: str, state: str | None = None) -> ApiResult[contracts.ConnectedAccount]:
        payload = {"code": code}
        if state:
            payload["state"] = state
        return await self._client._request(
            "POST", f"{API_PREFIX}/threads/connect/callback", json=payload, response_model=contracts.ConnectedAccount
        )

    async def list_accounts(
        self,
        *,
        ownership: str | None = None,
        status: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> ApiResult[contracts.Page[contracts.ConnectedAccount]]:
        params: dict[str, Any] = {}
        if ownership:
            params["ownership"] = ownership
        if status:
            params["status"] = status
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/threads/accounts",
            params=params or None,
            response_model=contracts.Page[contracts.ConnectedAccount],
        )

    async def account_detail(self, *, account_id: str) -> ApiResult[contracts.ConnectedAccount]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/threads/accounts/{account_id}", response_model=contracts.ConnectedAccount
        )

    async def disconnect_account(self, *, account_id: str) -> ApiResult[contracts.ConnectedAccount]:
        payload = {"account_id": account_id}
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/threads/accounts/disconnect",
            json=payload,
            response_model=contracts.ConnectedAccount,
        )

    async def ban_account(self, *, account_id: str) -> ApiResult[contracts.ConnectedAccount]:
        payload = {"account_id": account_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/threads/accounts/ban", json=payload, response_model=contracts.ConnectedAccount
        )

    async def assign_org(self, *, account_id: str, org_id: str) -> ApiResult[contracts.ConnectedAccount]:
        payload = {"account_id": account_id, "org_id": org_id}
        return await self._client._request(
            "POST", f"{API_PREFIX}/threads/accounts/assign-org", json=payload, response_model=contracts.ConnectedAccount
        )

    async def unassign_org(self, *, account_id: str) -> ApiResult[contracts.ConnectedAccount]:
        payload = {"account_id": account_id}
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/threads/accounts/unassign-org",
            json=payload,
            response_model=contracts.ConnectedAccount,
        )

    async def set_label(self, *, account_id: str, label: str | None = None) -> ApiResult[contracts.ConnectedAccount]:
        payload = {"account_id": account_id, "label": label}
        return await self._client._request(
            "POST", f"{API_PREFIX}/threads/accounts/label", json=payload, response_model=contracts.ConnectedAccount
        )

    async def map_model_identity(
        self, request: ModelIdentityMapRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ConnectedAccount]:
        payload = self._payload(ModelIdentityMapRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/threads/accounts/map-model", json=payload, response_model=contracts.ConnectedAccount
        )

    async def set_icon(self, *, account_id: str, icon_url: str | None = None) -> ApiResult[contracts.ConnectedAccount]:
        payload: dict[str, Any] = {"account_id": account_id}
        if icon_url is not None:
            payload["icon_url"] = icon_url
        return await self._client._request(
            "POST", f"{API_PREFIX}/threads/accounts/icon", json=payload,
            response_model=contracts.ConnectedAccount,
        )


class WebhooksApi(_ServiceBase):
    async def health(self, headers: Mapping[str, str] | None = None) -> ApiResult[HealthStatus]:
        return await self._client._request(
            "GET", "/health", headers=headers, response_model=HealthStatus, use_webhooks=True
        )


class WorkflowsApi(_ServiceBase):
    async def list(
        self, request: contracts.WorkflowListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.WorkflowResponse]]:
        params = self._payload(contracts.WorkflowListQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/workflows",
            params=params or None,
            response_model=contracts.Page[contracts.WorkflowResponse],
        )

    async def get(self, *, workflow_id: str) -> ApiResult[contracts.WorkflowDetailResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/workflows/{workflow_id}", response_model=contracts.WorkflowDetailResponse
        )

    async def create(
        self, request: contracts.WorkflowCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.WorkflowDetailResponse]:
        payload = self._payload(contracts.WorkflowCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/workflows", json=payload, response_model=contracts.WorkflowDetailResponse
        )

    async def update(
        self, *, workflow_id: str, request: contracts.WorkflowUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.WorkflowDetailResponse]:
        payload = self._payload(contracts.WorkflowUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH",
            f"{API_PREFIX}/workflows/{workflow_id}",
            json=payload,
            response_model=contracts.WorkflowDetailResponse,
        )

    async def delete(self, *, workflow_id: str) -> ApiResult[dict]:
        return await self._client._request("DELETE", f"{API_PREFIX}/workflows/{workflow_id}", response_model=dict)

    async def duplicate(
        self, *, workflow_id: str, name: str | None = None
    ) -> ApiResult[contracts.WorkflowDetailResponse]:
        payload = {"name": name} if name else {}
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/workflows/{workflow_id}/duplicate",
            json=payload,
            response_model=contracts.WorkflowDetailResponse,
        )

    async def run(
        self, *, workflow_id: str, request: contracts.WorkflowRunRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.WorkflowRunResponse]:
        payload = self._payload(contracts.WorkflowRunRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/workflows/{workflow_id}/run",
            json=payload,
            response_model=contracts.WorkflowRunResponse,
        )

    async def batch_run(
        self, *, workflow_id: str, request: contracts.WorkflowBatchRunRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.WorkflowBatchRunResponse]:
        payload = self._payload(contracts.WorkflowBatchRunRequest, request, **kwargs)
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/workflows/{workflow_id}/batch-run",
            json=payload,
            response_model=contracts.WorkflowBatchRunResponse,
        )

    async def get_run(self, *, run_id: str) -> ApiResult[contracts.WorkflowRunResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/workflow-runs/{run_id}", response_model=contracts.WorkflowRunResponse
        )

    async def cancel_run(self, *, run_id: str) -> ApiResult[contracts.WorkflowRunResponse]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/workflow-runs/{run_id}/cancel", response_model=contracts.WorkflowRunResponse
        )

    async def list_runs(
        self, *, workflow_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.WorkflowRunResponse]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/workflows/{workflow_id}/runs",
            params=params or None,
            response_model=contracts.Page[contracts.WorkflowRunResponse],
        )

    async def get_batch_run(self, *, batch_run_id: str) -> ApiResult[contracts.WorkflowBatchRunResponse]:
        return await self._client._request(
            "GET",
            f"{API_PREFIX}/workflow-batch-runs/{batch_run_id}",
            response_model=contracts.WorkflowBatchRunResponse,
        )

    async def approve_step(self, *, step_id: str) -> ApiResult[contracts.WorkflowRunResponse]:
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/workflow-runs/run-steps/{step_id}/approve",
            json={},
            response_model=contracts.WorkflowRunResponse,
        )

    async def reject_step(
        self, *, step_id: str, reason: str | None = None
    ) -> ApiResult[contracts.WorkflowRunResponse]:
        return await self._client._request(
            "POST",
            f"{API_PREFIX}/workflow-runs/run-steps/{step_id}/reject",
            json={"reason": reason} if reason else {},
            response_model=contracts.WorkflowRunResponse,
        )

    async def update_step_inputs(
        self, *, step_id: str, inputs: dict
    ) -> ApiResult[contracts.WorkflowRunStepResponse]:
        return await self._client._request(
            "PATCH",
            f"{API_PREFIX}/workflow-runs/run-steps/{step_id}/inputs",
            json={"inputs": inputs},
            response_model=contracts.WorkflowRunStepResponse,
        )


class PushSubscriptionsApi(_ServiceBase):

    async def vapid_public_key(self) -> ApiResult[contracts.VapidPublicKeyResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/push-subscriptions/vapid-public-key",
            response_model=contracts.VapidPublicKeyResponse,
        )

    async def create(
        self, *, request: contracts.PushSubscriptionCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.PushSubscriptionResponse]:
        payload = self._payload(contracts.PushSubscriptionCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/push-subscriptions/",
            json=payload,
            response_model=contracts.PushSubscriptionResponse,
        )

    async def list(self) -> ApiResult[list[contracts.PushSubscriptionResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/push-subscriptions/",
            response_model=list[contracts.PushSubscriptionResponse],
        )

    async def delete(self, *, subscription_id: str) -> ApiResult[dict]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/push-subscriptions/{subscription_id}",
            response_model=dict,
        )


class AlbumsApi(_ServiceBase):
    async def list(
        self, request: contracts.AlbumListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.AlbumResponse]]:
        params = self._payload(contracts.AlbumListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/albums", params=params or None,
            response_model=contracts.Page[contracts.AlbumResponse],
        )

    async def create(
        self, request: contracts.AlbumCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.AlbumResponse]:
        payload = self._payload(contracts.AlbumCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/albums", json=payload, response_model=contracts.AlbumResponse
        )

    async def get(
        self, *, album_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.AlbumDetailResponse]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/albums/{album_id}", params=params or None,
            response_model=contracts.AlbumDetailResponse,
        )

    async def update(
        self, *, album_id: str, request: contracts.AlbumUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.AlbumResponse]:
        payload = self._payload(contracts.AlbumUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/albums/{album_id}", json=payload, response_model=contracts.AlbumResponse
        )

    async def delete(self, *, album_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/albums/{album_id}", response_model=DeletionResult
        )

    async def list_items(
        self, *, album_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.AlbumItemResponse]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/albums/{album_id}/items", params=params or None,
            response_model=contracts.Page[contracts.AlbumItemResponse],
        )

    async def add_item(
        self, request: contracts.AlbumItemCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.AlbumItemResponse]:
        payload = self._payload(contracts.AlbumItemCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/albums/items", json=payload, response_model=contracts.AlbumItemResponse
        )

    async def bulk_add_items(self, *, album_id: str, items: list[dict]) -> ApiResult[list[contracts.AlbumItemResponse]]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/albums/items/bulk", json={"album_id": album_id, "items": items},
            response_model=list[contracts.AlbumItemResponse],
        )

    async def update_item(
        self, *, item_id: str, request: contracts.AlbumItemUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.AlbumItemResponse]:
        payload = self._payload(contracts.AlbumItemUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/albums/items/{item_id}", json=payload, response_model=contracts.AlbumItemResponse
        )

    async def remove_item(self, *, item_id: str) -> ApiResult[DeletionResult]:
        payload = self._payload(contracts.AlbumItemRemoveRequest, None, item_id=item_id)
        return await self._client._request(
            "POST", f"{API_PREFIX}/albums/items/remove", json=payload, response_model=DeletionResult
        )

    async def link(
        self, request: contracts.AlbumLinkRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.AlbumLinkResponse]:
        payload = self._payload(contracts.AlbumLinkRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/albums/link", json=payload, response_model=contracts.AlbumLinkResponse
        )

    async def unlink(self, *, album_id: str, model_id: str) -> ApiResult[DeletionResult]:
        payload = self._payload(contracts.AlbumUnlinkRequest, None, album_id=album_id, model_id=model_id)
        return await self._client._request(
            "POST", f"{API_PREFIX}/albums/unlink", json=payload, response_model=DeletionResult
        )

    async def share(
        self, request: contracts.AlbumShareRequest | None = None, **kwargs: Any
    ) -> ApiResult[ModelShareGrant]:
        payload = self._payload(contracts.AlbumShareRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/albums/share", json=payload, response_model=ModelShareGrant
        )

    async def revoke(self, *, grant_id: str) -> ApiResult[RevokedResult]:
        payload = self._payload(contracts.AlbumRevokeRequest, None, grant_id=grant_id)
        return await self._client._request(
            "POST", f"{API_PREFIX}/albums/revoke", json=payload, response_model=RevokedResult
        )

    async def shares(
        self, *, album_id: str, request: contracts.PaginationQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[ModelShareGrant]]:
        params = self._payload(contracts.PaginationQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/albums/{album_id}/shares", params=params or None,
            response_model=contracts.Page[ModelShareGrant],
        )


class VisionApi(_ServiceBase):
    async def face_swap(
        self, request: contracts.FaceSwapRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.FaceSwapRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/vision/face-swap", json=payload, response_model=contracts.JobResponse
        )

    async def image_crop(
        self, request: contracts.ImageCropRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.ImageCropRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/vision/image-crop", json=payload, response_model=contracts.JobResponse
        )

    async def seedream(
        self, request: contracts.SeedreamRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.SeedreamRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/vision/seedream", json=payload, response_model=contracts.JobResponse
        )

    async def topaz(
        self, request: contracts.TopazRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.TopazRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/vision/topaz", json=payload, response_model=contracts.JobResponse
        )

    async def nano_banana(
        self, request: contracts.NanoBananaRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.NanoBananaRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/vision/nano-banana", json=payload, response_model=contracts.JobResponse
        )

    async def sora(
        self, request: contracts.SoraRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.SoraRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/vision/sora", json=payload, response_model=contracts.JobResponse
        )

    async def kling(
        self, request: contracts.KlingRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.KlingRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/vision/kling", json=payload, response_model=contracts.JobResponse
        )

    async def grok(
        self, request: contracts.GrokRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.GrokRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/vision/grok", json=payload, response_model=contracts.JobResponse
        )

    async def flux(
        self, request: contracts.FluxRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.JobResponse]:
        payload = self._payload(contracts.FluxRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/vision/flux", json=payload, response_model=contracts.JobResponse
        )


class TikTokApi(_ServiceBase):
    async def connect_start(self) -> ApiResult[contracts.TiktokConnectStartResponse]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/connect/start", json={},
            response_model=contracts.TiktokConnectStartResponse,
        )

    async def connect_callback(
        self, *, code: str, state: str | None = None,
        request: contracts.TiktokConnectCallbackPayload | None = None, **kwargs: Any
    ) -> ApiResult[contracts.TiktokConnectedAccount]:
        payload = self._payload(contracts.TiktokConnectCallbackPayload, request, code=code, state=state)
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/connect/callback", json=payload,
            response_model=contracts.TiktokConnectedAccount,
        )

    async def refresh_tokens(
        self, *, connected_account_id: str, refresh_token: str
    ) -> ApiResult[contracts.TiktokTokenRefreshResponse]:
        payload = {"connected_account_id": connected_account_id, "refresh_token": refresh_token}
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/tokens/refresh", json=payload,
            response_model=contracts.TiktokTokenRefreshResponse,
        )

    async def list_accounts(
        self, *, ownership: str | None = None, status: str | None = None,
        page: int | None = None, page_size: int | None = None
    ) -> ApiResult[contracts.Page[contracts.TiktokConnectedAccount]]:
        params: dict[str, Any] = {}
        if ownership: params["ownership"] = ownership
        if status: params["status"] = status
        if page: params["page"] = page
        if page_size: params["page_size"] = page_size
        return await self._client._request(
            "GET", f"{API_PREFIX}/tiktok/accounts", params=params or None,
            response_model=contracts.Page[contracts.TiktokConnectedAccount],
        )

    async def account_detail(self, *, account_id: str) -> ApiResult[contracts.TiktokConnectedAccount]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/tiktok/accounts/{account_id}",
            response_model=contracts.TiktokConnectedAccount,
        )

    async def disconnect_account(self, *, account_id: str) -> ApiResult[contracts.TiktokConnectedAccount]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/accounts/disconnect", json={"account_id": account_id},
            response_model=contracts.TiktokConnectedAccount,
        )

    async def ban_account(self, *, account_id: str) -> ApiResult[contracts.TiktokConnectedAccount]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/accounts/ban", json={"account_id": account_id},
            response_model=contracts.TiktokConnectedAccount,
        )

    async def assign_org(self, *, account_id: str, org_id: str) -> ApiResult[contracts.TiktokConnectedAccount]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/accounts/assign-org",
            json={"account_id": account_id, "org_id": org_id},
            response_model=contracts.TiktokConnectedAccount,
        )

    async def unassign_org(self, *, account_id: str) -> ApiResult[contracts.TiktokConnectedAccount]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/accounts/unassign-org", json={"account_id": account_id},
            response_model=contracts.TiktokConnectedAccount,
        )

    async def set_label(self, *, account_id: str, label: str | None = None) -> ApiResult[contracts.TiktokConnectedAccount]:
        payload: dict[str, Any] = {"account_id": account_id}
        if label is not None: payload["label"] = label
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/accounts/label", json=payload,
            response_model=contracts.TiktokConnectedAccount,
        )

    async def set_icon(self, *, account_id: str, icon_url: str | None = None) -> ApiResult[contracts.TiktokConnectedAccount]:
        payload: dict[str, Any] = {"account_id": account_id}
        if icon_url is not None: payload["icon_url"] = icon_url
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/accounts/icon", json=payload,
            response_model=contracts.TiktokConnectedAccount,
        )

    async def map_model(
        self, request: ModelIdentityMapRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.TiktokConnectedAccount]:
        payload = self._payload(ModelIdentityMapRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/accounts/map-model", json=payload,
            response_model=contracts.TiktokConnectedAccount,
        )

    async def unmap_model(self, *, account_id: str, model_id: str) -> ApiResult[contracts.TiktokConnectedAccount]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/accounts/unmap-model",
            json={"account_id": account_id, "model_id": model_id},
            response_model=contracts.TiktokConnectedAccount,
        )

    async def list_videos(
        self, *, account_id: str, request: contracts.TiktokVideoListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.TiktokVideo]]:
        params = self._payload(contracts.TiktokVideoListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/tiktok/accounts/{account_id}/videos", params=params or None,
            response_model=contracts.Page[contracts.TiktokVideo],
        )

    async def link_job_to_video(
        self, *, video_id: str, request: contracts.TiktokVideoJobLinkRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.TiktokVideoJobLink]:
        payload = self._payload(contracts.TiktokVideoJobLinkRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/tiktok/videos/{video_id}/job-links", json=payload,
            response_model=contracts.TiktokVideoJobLink,
        )

    async def analytics(
        self, request: contracts.TiktokAnalyticsQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.TiktokAnalyticsResponse]:
        params = self._payload(contracts.TiktokAnalyticsQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/tiktok/analytics", params=params or None,
            response_model=contracts.TiktokAnalyticsResponse,
        )


class ReferralsApi(_ServiceBase):
    async def summary(self) -> ApiResult[contracts.ReferralSummaryResult]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/referrals/summary", response_model=contracts.ReferralSummaryResult
        )

    async def list_codes(self) -> ApiResult[list[contracts.ReferralCodeResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/referrals/codes", response_model=list[contracts.ReferralCodeResponse]
        )

    async def create_code(self) -> ApiResult[contracts.ReferralCodeResponse]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/referrals/codes", json={}, response_model=contracts.ReferralCodeResponse
        )

    async def revoke_code(self, *, code_id: str) -> ApiResult[contracts.ReferralCodeResponse]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/referrals/codes/{code_id}/revoke", json={},
            response_model=contracts.ReferralCodeResponse,
        )


class HuggingFaceApi(_ServiceBase):
    async def list_keys(self) -> ApiResult[list[contracts.HfKeyResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/huggingface/keys", response_model=list[contracts.HfKeyResponse]
        )

    async def create_key(
        self, request: contracts.HfKeyCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.HfKeyResponse]:
        payload = self._payload(contracts.HfKeyCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/huggingface/keys", json=payload, response_model=contracts.HfKeyResponse
        )

    async def update_key(
        self, *, key_id: str, request: contracts.HfKeyUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.HfKeyResponse]:
        payload = self._payload(contracts.HfKeyUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/huggingface/keys/{key_id}", json=payload, response_model=contracts.HfKeyResponse
        )

    async def delete_key(self, *, key_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/huggingface/keys/{key_id}", response_model=DeletionResult
        )

    async def share_key(
        self, request: contracts.HfKeyShareRequest | None = None, **kwargs: Any
    ) -> ApiResult[ModelShareGrant]:
        payload = self._payload(contracts.HfKeyShareRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/huggingface/keys/share", json=payload, response_model=ModelShareGrant
        )

    async def revoke_key(self, *, grant_id: str) -> ApiResult[RevokedResult]:
        payload = self._payload(contracts.KeyShareRevokeRequest, None, grant_id=grant_id)
        return await self._client._request(
            "POST", f"{API_PREFIX}/huggingface/keys/revoke", json=payload, response_model=RevokedResult
        )

    async def list_shares(self, *, key_id: str) -> ApiResult[list[ModelShareGrant]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/huggingface/keys/{key_id}/shares", response_model=list[ModelShareGrant]
        )

    async def probe_repo(self, *, repo_url: str, hf_api_key_id: str | None = None) -> ApiResult[dict]:
        payload: dict[str, Any] = {"repo_url": repo_url}
        if hf_api_key_id: payload["hf_api_key_id"] = hf_api_key_id
        return await self._client._request(
            "POST", f"{API_PREFIX}/huggingface/repo-info", json=payload, response_model=dict
        )


class CivitaiApi(_ServiceBase):
    async def list_keys(self) -> ApiResult[list[contracts.CivitaiKeyResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/civitai/keys", response_model=list[contracts.CivitaiKeyResponse]
        )

    async def create_key(
        self, request: contracts.CivitaiKeyCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CivitaiKeyResponse]:
        payload = self._payload(contracts.CivitaiKeyCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/civitai/keys", json=payload, response_model=contracts.CivitaiKeyResponse
        )

    async def update_key(
        self, *, key_id: str, request: contracts.CivitaiKeyUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.CivitaiKeyResponse]:
        payload = self._payload(contracts.CivitaiKeyUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/civitai/keys/{key_id}", json=payload, response_model=contracts.CivitaiKeyResponse
        )

    async def delete_key(self, *, key_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/civitai/keys/{key_id}", response_model=DeletionResult
        )

    async def share_key(
        self, request: contracts.CivitaiKeyShareRequest | None = None, **kwargs: Any
    ) -> ApiResult[ModelShareGrant]:
        payload = self._payload(contracts.CivitaiKeyShareRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/civitai/keys/share", json=payload, response_model=ModelShareGrant
        )

    async def revoke_key(self, *, grant_id: str) -> ApiResult[RevokedResult]:
        payload = self._payload(contracts.KeyShareRevokeRequest, None, grant_id=grant_id)
        return await self._client._request(
            "POST", f"{API_PREFIX}/civitai/keys/revoke", json=payload, response_model=RevokedResult
        )

    async def list_shares(self, *, key_id: str) -> ApiResult[list[ModelShareGrant]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/civitai/keys/{key_id}/shares", response_model=list[ModelShareGrant]
        )


class ElevenLabsApi(_ServiceBase):
    async def list_keys(self) -> ApiResult[list[contracts.ElevenLabsKeyResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/elevenlabs/keys", response_model=list[contracts.ElevenLabsKeyResponse]
        )

    async def create_key(
        self, request: contracts.ElevenLabsKeyCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ElevenLabsKeyResponse]:
        payload = self._payload(contracts.ElevenLabsKeyCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/elevenlabs/keys", json=payload, response_model=contracts.ElevenLabsKeyResponse
        )

    async def update_key(
        self, *, key_id: str, request: contracts.ElevenLabsKeyUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ElevenLabsKeyResponse]:
        payload = self._payload(contracts.ElevenLabsKeyUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/elevenlabs/keys/{key_id}", json=payload, response_model=contracts.ElevenLabsKeyResponse
        )

    async def delete_key(self, *, key_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/elevenlabs/keys/{key_id}", response_model=DeletionResult
        )

    async def share_key(
        self, request: contracts.ElevenLabsKeyShareRequest | None = None, **kwargs: Any
    ) -> ApiResult[ModelShareGrant]:
        payload = self._payload(contracts.ElevenLabsKeyShareRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/elevenlabs/keys/share", json=payload, response_model=ModelShareGrant
        )

    async def revoke_key(self, *, grant_id: str) -> ApiResult[RevokedResult]:
        payload = self._payload(contracts.KeyShareRevokeRequest, None, grant_id=grant_id)
        return await self._client._request(
            "POST", f"{API_PREFIX}/elevenlabs/keys/revoke", json=payload, response_model=RevokedResult
        )

    async def list_shares(self, *, key_id: str) -> ApiResult[list[ModelShareGrant]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/elevenlabs/keys/{key_id}/shares", response_model=list[ModelShareGrant]
        )

    async def list_models(self, *, key_id: str) -> ApiResult[list[contracts.ElevenLabsModelResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/elevenlabs/models", params={"key_id": key_id},
            response_model=list[contracts.ElevenLabsModelResponse],
        )

    async def list_voices(
        self, request: contracts.ElevenLabsVoiceListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.ElevenLabsVoiceResponse]]:
        params = self._payload(contracts.ElevenLabsVoiceListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/elevenlabs/voices", params=params or None,
            response_model=contracts.Page[contracts.ElevenLabsVoiceResponse],
        )

    async def get_voice(self, *, voice_id: str, key_id: str) -> ApiResult[contracts.ElevenLabsVoiceResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/elevenlabs/voices/{voice_id}", params={"key_id": key_id},
            response_model=contracts.ElevenLabsVoiceResponse,
        )

    async def voice_model_links(self, *, voice_id: str, key_id: str) -> ApiResult[list[str]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/elevenlabs/voices/{voice_id}/models", params={"key_id": key_id},
            response_model=list[str],
        )

    async def update_voice_model_links(
        self, *, voice_id: str, request: contracts.ElevenLabsVoiceModelLinksUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[dict]:
        payload = self._payload(contracts.ElevenLabsVoiceModelLinksUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PUT", f"{API_PREFIX}/elevenlabs/voices/{voice_id}/models", json=payload, response_model=dict
        )

    async def clone_voice(
        self, request: contracts.ElevenLabsVoiceCloneRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ElevenLabsVoiceResponse]:
        payload = self._payload(contracts.ElevenLabsVoiceCloneRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/elevenlabs/voices/clone", json=payload,
            response_model=contracts.ElevenLabsVoiceResponse,
        )

    async def design_voice(
        self, request: contracts.ElevenLabsVoiceDesignRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ElevenLabsVoiceDesignResponse]:
        payload = self._payload(contracts.ElevenLabsVoiceDesignRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/elevenlabs/voices/design", json=payload,
            response_model=contracts.ElevenLabsVoiceDesignResponse,
        )

    async def update_voice(
        self, *, voice_id: str, request: contracts.ElevenLabsVoiceUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ElevenLabsVoiceResponse]:
        payload = self._payload(contracts.ElevenLabsVoiceUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/elevenlabs/voices/{voice_id}", json=payload,
            response_model=contracts.ElevenLabsVoiceResponse,
        )

    async def delete_voice(self, *, voice_id: str, key_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/elevenlabs/voices/{voice_id}", params={"key_id": key_id},
            response_model=DeletionResult,
        )

    async def voice_settings(self, *, voice_id: str, key_id: str) -> ApiResult[dict]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/elevenlabs/voices/{voice_id}/settings", params={"key_id": key_id},
            response_model=dict,
        )

    async def update_voice_settings(
        self, *, voice_id: str, request: contracts.ElevenLabsVoiceSettingsUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[dict]:
        payload = self._payload(contracts.ElevenLabsVoiceSettingsUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/elevenlabs/voices/{voice_id}/settings", json=payload, response_model=dict
        )

    async def text_to_speech(
        self, request: contracts.ElevenLabsTtsRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.ElevenLabsSpeechResponse]:
        payload = self._payload(contracts.ElevenLabsTtsRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/elevenlabs/speech", json=payload,
            response_model=contracts.ElevenLabsSpeechResponse,
        )



class LegalApi(_ServiceBase):
    async def terms(self) -> ApiResult[contracts.LegalDocumentResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/legal/terms", response_model=contracts.LegalDocumentResponse
        )

    async def privacy(self) -> ApiResult[contracts.LegalDocumentResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/legal/privacy", response_model=contracts.LegalDocumentResponse
        )


class AppsApi(_ServiceBase):
    async def list(
        self, request: contracts.AppListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.AppCatalogItemResponse]]:
        params = self._payload(contracts.AppListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/apps", params=params or None,
            response_model=contracts.Page[contracts.AppCatalogItemResponse],
        )

    async def access(self, *, app_slug: str) -> ApiResult[contracts.AppAccessResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/apps/{app_slug}/access", response_model=contracts.AppAccessResponse
        )

    async def latest_version(self, *, app_slug: str) -> ApiResult[contracts.AppLatestVersionResponse]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/apps/{app_slug}/versions/latest",
            response_model=contracts.AppLatestVersionResponse,
        )

    async def list_versions(
        self, *, app_slug: str, request: contracts.AppVersionListQuery | None = None, **kwargs: Any
    ) -> ApiResult[contracts.Page[contracts.AppVersionPublicResponse]]:
        params = self._payload(contracts.AppVersionListQuery, request, **kwargs)
        return await self._client._request(
            "GET", f"{API_PREFIX}/apps/{app_slug}/versions", params=params or None,
            response_model=contracts.Page[contracts.AppVersionPublicResponse],
        )


class DiscordWebhooksApi(_ServiceBase):
    async def list(self, *, org_id: str) -> ApiResult[list[contracts.OrgDiscordWebhookResponse]]:
        return await self._client._request(
            "GET", f"{API_PREFIX}/orgs/{org_id}/discord-webhooks",
            response_model=list[contracts.OrgDiscordWebhookResponse],
        )

    async def create(
        self, *, org_id: str, request: contracts.OrgDiscordWebhookCreateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.OrgDiscordWebhookResponse]:
        payload = self._payload(contracts.OrgDiscordWebhookCreateRequest, request, **kwargs)
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/{org_id}/discord-webhooks", json=payload,
            response_model=contracts.OrgDiscordWebhookResponse,
        )

    async def update(
        self, *, org_id: str, webhook_id: str,
        request: contracts.OrgDiscordWebhookUpdateRequest | None = None, **kwargs: Any
    ) -> ApiResult[contracts.OrgDiscordWebhookResponse]:
        payload = self._payload(contracts.OrgDiscordWebhookUpdateRequest, request, **kwargs)
        return await self._client._request(
            "PATCH", f"{API_PREFIX}/orgs/{org_id}/discord-webhooks/{webhook_id}", json=payload,
            response_model=contracts.OrgDiscordWebhookResponse,
        )

    async def delete(self, *, org_id: str, webhook_id: str) -> ApiResult[DeletionResult]:
        return await self._client._request(
            "DELETE", f"{API_PREFIX}/orgs/{org_id}/discord-webhooks/{webhook_id}",
            response_model=DeletionResult,
        )

    async def test(
        self, *, org_id: str, webhook_id: str
    ) -> ApiResult[contracts.OrgDiscordWebhookTestResponse]:
        return await self._client._request(
            "POST", f"{API_PREFIX}/orgs/{org_id}/discord-webhooks/{webhook_id}/test", json={},
            response_model=contracts.OrgDiscordWebhookTestResponse,
        )


__all__ = ["InoueAiSaasClient"]
