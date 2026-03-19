"""Tests verifying all API classes are present and correctly wired."""

from __future__ import annotations

import pytest

from inoue_ai_saas_sdk import InoueAiSaasClient


ALL_API_NAMES = [
    "auth", "orgs", "models", "prompts", "jobs", "downloads", "credits",
    "billing", "admin_downloads", "internal", "assets", "posts", "schedule",
    "calendar_feeds", "webhooks", "fanvue", "threads", "collections",
    "pooling", "notifications", "analytics", "audit", "system", "workflows",
    "push_subscriptions", "albums", "vision", "tiktok", "referrals",
    "huggingface", "civitai", "elevenlabs", "loras", "legal", "apps",
    "discord_webhooks",
]


def test_client_has_all_api_accessors(client: InoueAiSaasClient) -> None:
    for name in ALL_API_NAMES:
        assert hasattr(client, name), f"Missing API accessor: {name}"
        assert getattr(client, name) is not None, f"API accessor is None: {name}"


def test_client_api_count(client: InoueAiSaasClient) -> None:
    assert len(ALL_API_NAMES) == 36


# --- Existing API classes: verify new methods exist ---

NEW_AUTH_METHODS = ["register_settings", "logout", "update_me", "me_analytics", "me_storage"]
NEW_ORGS_METHODS = ["bulk_update", "list_org_notifications", "org_storage"]
NEW_MODELS_METHODS = [
    "character_schema", "create_character_creation", "list_character_creations",
    "get_character_creation", "patch_character_creation", "revoke_share", "model_replies",
]
NEW_JOBS_METHODS = ["save_output_asset"]
NEW_ASSETS_METHODS = ["upload_url", "retry_upload", "get_url", "get_content", "download", "bulk_update", "mark_delete"]
NEW_PROMPTS_METHODS = ["delete_template", "update_version_config", "unlink_template", "delete_run"]
NEW_DOWNLOADS_METHODS = ["delete"]
NEW_CREDITS_METHODS = ["usage_series"]
NEW_SCHEDULE_METHODS = [
    "list_recurring_rules", "create_recurring_rule", "update_recurring_rule",
    "delete_recurring_rule", "toggle_rule",
]
NEW_FANVUE_METHODS = ["mass_send", "delete_message", "heartbeat_conversation", "list_media", "fan_insights", "set_icon", "unmap_model"]
NEW_THREADS_METHODS = ["set_icon"]


@pytest.mark.parametrize("api_name,method_name", [
    *[("auth", m) for m in NEW_AUTH_METHODS],
    *[("orgs", m) for m in NEW_ORGS_METHODS],
    *[("models", m) for m in NEW_MODELS_METHODS],
    *[("jobs", m) for m in NEW_JOBS_METHODS],
    *[("assets", m) for m in NEW_ASSETS_METHODS],
    *[("prompts", m) for m in NEW_PROMPTS_METHODS],
    *[("downloads", m) for m in NEW_DOWNLOADS_METHODS],
    *[("credits", m) for m in NEW_CREDITS_METHODS],
    *[("schedule", m) for m in NEW_SCHEDULE_METHODS],
    *[("fanvue", m) for m in NEW_FANVUE_METHODS],
    *[("threads", m) for m in NEW_THREADS_METHODS],
])
def test_existing_api_has_new_method(client: InoueAiSaasClient, api_name: str, method_name: str) -> None:
    api = getattr(client, api_name)
    assert hasattr(api, method_name), f"{api_name}.{method_name} missing"
    assert callable(getattr(api, method_name)), f"{api_name}.{method_name} not callable"


# --- New API classes: verify key methods exist ---

NEW_API_METHOD_MAP = {
    "albums": ["list", "create", "get", "update", "delete", "list_items", "add_item", "share", "revoke", "shares"],
    "vision": ["face_swap", "image_crop", "seedream", "topaz", "nano_banana", "sora", "kling", "grok", "flux"],
    "tiktok": ["connect_start", "connect_callback", "list_accounts", "account_detail", "disconnect_account", "analytics"],
    "referrals": ["summary", "list_codes", "create_code", "revoke_code"],
    "huggingface": ["list_keys", "create_key", "update_key", "delete_key", "share_key", "list_shares", "probe_repo"],
    "civitai": ["list_keys", "create_key", "update_key", "delete_key", "share_key", "list_shares"],
    "elevenlabs": [
        "list_keys", "create_key", "list_models", "list_voices", "get_voice",
        "clone_voice", "design_voice", "update_voice", "delete_voice", "text_to_speech",
    ],
    "loras": ["list", "create", "update", "delete"],
    "legal": ["terms", "privacy"],
    "apps": ["list", "access", "latest_version", "list_versions"],
    "discord_webhooks": ["list", "create", "update", "delete", "test"],
}


@pytest.mark.parametrize("api_name,method_name", [
    (api, method)
    for api, methods in NEW_API_METHOD_MAP.items()
    for method in methods
])
def test_new_api_has_method(client: InoueAiSaasClient, api_name: str, method_name: str) -> None:
    api = getattr(client, api_name)
    assert hasattr(api, method_name), f"{api_name}.{method_name} missing"
    assert callable(getattr(api, method_name)), f"{api_name}.{method_name} not callable"
