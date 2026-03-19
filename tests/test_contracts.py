"""Tests verifying all new contract models import and validate correctly."""

from __future__ import annotations

import pytest


def test_new_contract_modules_import() -> None:
    from inoue_ai_saas_contracts import referrals  # noqa: F401
    from inoue_ai_saas_contracts import apps  # noqa: F401
    from inoue_ai_saas_contracts import tiktok  # noqa: F401
    from inoue_ai_saas_contracts import vision  # noqa: F401
    from inoue_ai_saas_contracts import elevenlabs  # noqa: F401


def test_referral_contracts() -> None:
    from inoue_ai_saas_contracts import ReferralSummaryResult, ReferralCodeResponse

    summary = ReferralSummaryResult(
        users_per_reward=5, credits_per_reward=100, max_codes_per_user=3,
        referred_users_count=10, earned_credits_total=500, rewards_earned_count=2,
        active_codes_count=1, pending_users_count=3, next_reward_users_remaining=2,
    )
    assert summary.credits_per_reward == 100

    code = ReferralCodeResponse(id="abc", code="MYCODE", code_hint="MY***", uses_count=5, status="active")
    assert code.status == "active"


def test_app_contracts() -> None:
    from inoue_ai_saas_contracts import AppCatalogItemResponse, AppAccessResponse

    item = AppCatalogItemResponse(id="1", slug="myapp", name="My App")
    assert item.slug == "myapp"

    access = AppAccessResponse(allowed=True)
    assert access.allowed is True


def test_tiktok_contracts() -> None:
    from inoue_ai_saas_contracts import TiktokConnectStartResponse, TiktokVideo

    start = TiktokConnectStartResponse(url="https://tiktok.com/oauth", state="abc", mode="connect")
    assert start.mode == "connect"

    video = TiktokVideo(id="v1", connected_account_id="acc1", remote_video_id="rv1")
    assert video.connected_account_id == "acc1"


def test_vision_contracts() -> None:
    from inoue_ai_saas_contracts import FaceSwapRequest, SeedreamRequest, FluxRequest
    from inoue_ai_saas_contracts.enums import JobType

    fs = FaceSwapRequest(source_asset_id="src1", target_asset_ids=["t1", "t2"])
    assert len(fs.target_asset_ids) == 2

    sd = SeedreamRequest(job_type=JobType.SEEDREAM_V4_T2I, prompt="test")
    assert sd.prompt == "test"


def test_elevenlabs_contracts() -> None:
    from inoue_ai_saas_contracts import ElevenLabsVoiceResponse, ElevenLabsTtsRequest

    voice = ElevenLabsVoiceResponse(voice_id="v1", name="Test Voice")
    assert voice.voice_id == "v1"

    tts = ElevenLabsTtsRequest(key_id="k1", model_id="m1", voice_id="v1", text="Hello")
    assert tts.text == "Hello"


def test_legal_contracts() -> None:
    from inoue_ai_saas_contracts import LegalDocumentResponse, LegalDocumentSection
    from datetime import date

    section = LegalDocumentSection(heading="Terms", body=["paragraph 1"])
    doc = LegalDocumentResponse(
        key="terms", title="Terms of Service", version="1.0",
        effective_date=date(2025, 1, 1), summary="Terms summary",
        sections=[section],
    )
    assert doc.key == "terms"
    assert len(doc.sections) == 1


def test_elevenlabs_key_contracts_exported() -> None:
    from inoue_ai_saas_contracts import (
        ElevenLabsKeyCreateRequest,
        ElevenLabsKeyResponse,
        ElevenLabsKeyUpdateRequest,
        ElevenLabsKeyShareRequest,
    )
    key = ElevenLabsKeyCreateRequest(label="test", token="tok")
    assert key.label == "test"


def test_discord_webhook_contracts() -> None:
    from inoue_ai_saas_contracts import OrgDiscordWebhookCreateRequest, OrgDiscordWebhookResponse

    req = OrgDiscordWebhookCreateRequest(name="Alerts", webhook_url="https://discord.com/api/webhooks/123")
    assert req.name == "Alerts"
