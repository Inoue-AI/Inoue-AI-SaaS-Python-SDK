"""Tests verifying new API methods build correct HTTP requests."""

from __future__ import annotations

import json

import pytest

from inoue_ai_saas_sdk import InoueAiSaasClient
from tests.conftest import MockTransport


@pytest.fixture()
def transport():
    return MockTransport(data={})


@pytest.fixture()
def sdk(transport: MockTransport) -> InoueAiSaasClient:
    return InoueAiSaasClient(
        "https://api.test",
        access_token="tok",
        transport=transport,
        webhooks_transport=transport,
    )


@pytest.mark.asyncio
async def test_legal_terms_sends_get(sdk: InoueAiSaasClient, transport: MockTransport) -> None:
    transport._data = {
        "key": "terms", "title": "Terms", "version": "1.0",
        "effective_date": "2025-01-01", "summary": "s", "sections": [],
    }
    result = await sdk.legal.terms()
    assert transport.last_request is not None
    assert transport.last_request.method == "GET"
    assert "/v1/legal/terms" in str(transport.last_request.url)


@pytest.mark.asyncio
async def test_referrals_summary_sends_get(sdk: InoueAiSaasClient, transport: MockTransport) -> None:
    transport._data = {
        "users_per_reward": 5, "credits_per_reward": 100, "max_codes_per_user": 3,
        "referred_users_count": 0, "earned_credits_total": 0, "rewards_earned_count": 0,
        "active_codes_count": 0, "pending_users_count": 0, "next_reward_users_remaining": 5,
    }
    result = await sdk.referrals.summary()
    assert transport.last_request.method == "GET"
    assert "/v1/referrals/summary" in str(transport.last_request.url)
    assert result.data.credits_per_reward == 100


@pytest.mark.asyncio
async def test_vision_face_swap_sends_post(sdk: InoueAiSaasClient, transport: MockTransport) -> None:
    transport._data = {"id": "j1", "job_type": "face_swap", "status": "queued"}
    result = await sdk.vision.face_swap(source_asset_id="src", target_asset_ids=["t1"])
    assert transport.last_request.method == "POST"
    assert "/v1/vision/face-swap" in str(transport.last_request.url)
    body = json.loads(transport.last_request.content)
    assert body["source_asset_id"] == "src"
    assert body["target_asset_ids"] == ["t1"]


@pytest.mark.asyncio
async def test_auth_logout_clears_tokens(sdk: InoueAiSaasClient, transport: MockTransport) -> None:
    transport._data = {}
    assert sdk.access_token == "tok"
    await sdk.auth.logout()
    assert sdk.access_token is None
    assert sdk.refresh_token is None


@pytest.mark.asyncio
async def test_discord_webhooks_create(sdk: InoueAiSaasClient, transport: MockTransport) -> None:
    transport._data = {
        "id": "wh1", "org_id": "org1", "name": "Alerts",
        "webhook_url": "https://discord.com/api/webhooks/123",
        "is_enabled": True, "event_types": [],
    }
    result = await sdk.discord_webhooks.create(
        org_id="org1", name="Alerts", webhook_url="https://discord.com/api/webhooks/123"
    )
    assert transport.last_request.method == "POST"
    assert "/v1/orgs/org1/discord-webhooks" in str(transport.last_request.url)


@pytest.mark.asyncio
async def test_schedule_create_recurring_rule(sdk: InoueAiSaasClient, transport: MockTransport) -> None:
    transport._data = {
        "id": "rule1", "event_type": "schedule_post", "label": "Daily",
        "recurrence": {}, "template": {}, "is_active": True,
    }
    import inoue_ai_saas_contracts as c
    result = await sdk.schedule.create_recurring_rule(
        event_type="schedule_post", label="Daily",
        recurrence=c.RecurrenceSchema(frequency="daily", time="09:00"),
    )
    assert transport.last_request.method == "POST"
    assert "/v1/schedule/recurring-rules" in str(transport.last_request.url)
