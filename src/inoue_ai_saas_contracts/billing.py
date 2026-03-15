from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

BillingProductType = Literal["subscription", "credits_bundle"]
BillingOrderType = Literal["subscription", "credits_bundle"]


class BillingFeatureLimits(BaseModel):
    subscription_type: str = "default"
    max_models_owned: int | None = None
    max_owned_organizations: int | None = None
    max_upload_storage_gb: Decimal | None = None
    max_connected_fanvue_accounts: int | None = None
    max_connected_tiktok_accounts: int | None = None
    max_monthly_download_urls: int | None = None


class BillingFeatureUsage(BaseModel):
    models_owned: int = 0
    owned_organizations: int = 0
    upload_storage_gb: Decimal = Decimal("0")
    connected_fanvue_accounts: int = 0
    connected_tiktok_accounts: int = 0
    monthly_download_urls: int = 0


class BillingProduct(BaseModel):
    product_id: str
    price_id: str
    name: str
    description: str | None = None
    currency: str
    unit_amount_cents: int | None = None
    interval: str | None = None
    interval_count: int | None = None
    type: BillingProductType
    credits_amount: Decimal
    subscription_type: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    product_active: bool = True
    price_active: bool = True


class BillingOrder(BaseModel):
    id: str
    order_type: BillingOrderType
    status: str
    currency: str | None = None
    amount_subtotal_cents: int | None = None
    amount_total_cents: int | None = None
    credits_amount: Decimal = Decimal("0")
    stripe_checkout_session_id: str | None = None
    stripe_invoice_id: str | None = None
    stripe_payment_intent_id: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class BillingSubscription(BaseModel):
    id: str
    stripe_subscription_id: str
    stripe_customer_id: str
    stripe_price_id: str
    stripe_product_id: str
    subscription_type: str | None = None
    status: str
    current_period_start: dt.datetime | None = None
    current_period_end: dt.datetime | None = None
    cancel_at_period_end: bool = False
    cancel_at: dt.datetime | None = None
    canceled_at: dt.datetime | None = None
    latest_invoice_id: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class BillingSummary(BaseModel):
    wallet_balance_credits: Decimal = Decimal("0")
    active_subscription: BillingSubscription | None = None
    active_subscription_type: str | None = None
    last_paid_order: BillingOrder | None = None
    pending_invoice: BillingOrder | None = None
    feature_limits: BillingFeatureLimits | None = None
    feature_usage: BillingFeatureUsage | None = None
    bundle_credits_only_mode: bool = False
    bundle_spendable_credits: Decimal | None = None


class BillingCheckoutCreateRequest(BaseModel):
    price_id: str
    success_url: str | None = None
    cancel_url: str | None = None


class BillingCheckoutCreateResult(BaseModel):
    checkout_url: str
    session_id: str


class BillingPortalCreateRequest(BaseModel):
    return_url: str | None = None


class BillingPortalCreateResult(BaseModel):
    portal_url: str


class BillingSubscriptionChangeRequest(BaseModel):
    price_id: str


class BillingSubscriptionChangeResult(BaseModel):
    subscription: BillingSubscription


class BillingSubscriptionTypeLimitUpsertRequest(BaseModel):
    max_models_owned: int | None = Field(default=None, gt=0)
    max_owned_organizations: int | None = Field(default=None, gt=0)
    max_upload_storage_gb: Decimal | None = Field(default=None, gt=0)
    max_connected_fanvue_accounts: int | None = Field(default=None, gt=0)
    max_connected_tiktok_accounts: int | None = Field(default=None, gt=0)
    max_monthly_download_urls: int | None = Field(default=None, gt=0)


class BillingSubscriptionTypeLimit(BillingFeatureLimits):
    created_by_user_id: str | None = None
    updated_by_user_id: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
