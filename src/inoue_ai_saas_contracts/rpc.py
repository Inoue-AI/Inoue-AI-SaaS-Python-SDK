from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TotpSecretRequest(BaseModel):
    user_id: str
    totp_secret: str
    recovery_codes_hashed: list[str]


class TotpSecretFetchRequest(BaseModel):
    user_id: str


class UpsertPlatformTokensRequest(BaseModel):
    connected_account_id: str = Field(..., alias="p_connected_account_id")
    access_token: str = Field(..., alias="p_access_token")
    refresh_token: str = Field(..., alias="p_refresh_token")
    token_expires_at: datetime | None = Field(None, alias="p_token_expires_at")

    model_config = ConfigDict(populate_by_name=True)


class CreateWebhookEndpointRequest(BaseModel):
    platform: str
    connected_account_id: str
    url: str
    secret: str | None = None
    is_enabled: bool = True
