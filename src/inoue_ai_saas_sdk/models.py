from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

import inoue_ai_saas_contracts as contracts
from inoue_ai_saas_contracts import (
    AcceptedResult,
    ApprovedResult,
    AssetPublicResponse,
    AuthMeOrg,
    AuthMeResult,
    BannedResult,
    DeclinedResult,
    DeletionResult,
    DeniedResult,
    DisconnectedResult,
    HealthStatus,
    JobCompletionResult,
    ModelIdentityMapRequest,
    ModelShareGrant,
    MutedResult,
    NotificationItem,
    OrgOverviewAudit,
    OrgOverviewMember,
    OrgOverviewResponse,
    Page,
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
from inoue_ai_saas_contracts.responses import ResponseMeta

T = TypeVar("T")


@dataclass
class ApiResult(Generic[T]):
    data: T
    meta: ResponseMeta
    trace_id: str | None = None


# Re-export commonly used models for SDK callers
__all__ = [
    "ApiResult",
    "DeletionResult",
    "TwoFactorSetupResult",
    "TwoFactorVerifyResult",
    "ModelIdentityMapRequest",
    "ModelShareGrant",
    "JobCompletionResult",
    "WebhookIngestResult",
    "WebhookEndpointCreateResult",
    "AuthMeOrg",
    "AuthMeResult",
    "RevenueSummary",
    "NotificationItem",
    "ReadResult",
    "UnreadResult",
    "MutedResult",
    "UnmutedResult",
    "AcceptedResult",
    "DeclinedResult",
    "RevokedResult",
    "ApprovedResult",
    "DeniedResult",
    "UnlockedResult",
    "DisconnectedResult",
    "BannedResult",
    "QuitResult",
    "HealthStatus",
    "JobResponse",
    "Page",
    "AssetPublicResponse",
    "OrgOverviewResponse",
    "OrgOverviewMember",
    "OrgOverviewAudit",
    "contracts",
]
