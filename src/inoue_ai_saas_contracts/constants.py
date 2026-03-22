from __future__ import annotations

API_VERSION = "v1"
API_PREFIX = "/v1"
INTERNAL_PREFIX = "/internal"

# Headers
HEADER_TRACE_ID = "X-Trace-Id"
HEADER_REQUEST_ID = "X-Request-Id"
HEADER_ADMIN_TOKEN = "X-Admin-Token"
HEADER_WORKER_BOOTSTRAP = "X-Worker-Bootstrap"

# Prompt run allowlist (source of truth)
from inoue_ai_saas_contracts.enums import EngineType, JobType  # noqa: E402

ALLOWED_PROMPT_RUN_JOB_TYPES = [
    # Legacy / RunPod serverless
    JobType.SDXL_IMAGE.value,
    JobType.UPSCALE.value,
    # Nano Banana
    JobType.NANOBANANA_T2I.value,
    JobType.NANOBANANA_I2I.value,
    JobType.NANOBANANA_PRO_T2I_1K2K.value,
    JobType.NANOBANANA_PRO_T2I_4K.value,
    JobType.NANOBANANA_PRO_I2I_1K2K.value,
    JobType.NANOBANANA_PRO_I2I_4K.value,
    # Seedream
    JobType.SEEDREAM_V4_T2I.value,
    JobType.SEEDREAM_V4_EDIT.value,
    JobType.SEEDREAM_V4_5_T2I.value,
    JobType.SEEDREAM_V4_5_EDIT.value,
    JobType.SEEDREAM_5_LITE_T2I.value,
    JobType.SEEDREAM_5_LITE_I2I.value,
    # Sora
    JobType.SORA2_T2V.value,
    JobType.SORA2_I2V.value,
    JobType.SORA2PRO_T2V.value,
    JobType.SORA2PRO_I2V.value,
    # Kling
    JobType.KLING_O1_T2V.value,
    JobType.KLING_O1_I2V.value,
    JobType.KLING_2_6_T2V.value,
    JobType.KLING_2_6_I2V.value,
    JobType.KLING_2_6_MOTION_V2V.value,
    JobType.KLING_2_5_TURBO_T2V.value,
    JobType.KLING_2_5_TURBO_I2V.value,
    JobType.KLING_2_1_MASTER_T2V.value,
    JobType.KLING_2_1_MASTER_I2V.value,
    JobType.KLING_2_1_T2V.value,
    JobType.KLING_2_1_I2V.value,
    JobType.KLING_2_0_T2V.value,
    JobType.KLING_2_0_I2V.value,
    JobType.KLING_3_0_VIDEO.value,
    # Grok Imagine
    JobType.GROK_IMAGINE_TEXT_TO_VIDEO.value,
    JobType.GROK_IMAGINE_IMAGE_TO_VIDEO.value,
    JobType.GROK_IMAGINE_IMAGE_TO_IMAGE.value,
    JobType.GROK_IMAGINE_TEXT_TO_IMAGE.value,
    # Topaz
    JobType.TOPAZ_IMAGE_UPSCALE.value,
    JobType.TOPAZ_VIDEO_UPSCALE.value,
    # Flux
    JobType.FLUX2_PRO_T2I.value,
    JobType.FLUX2_PRO_I2I.value,
    JobType.FLUX2_FLEX_T2I.value,
    JobType.FLUX2_FLEX_I2I.value,
    # Qwen / Wan / Z-Image (RunPod serverless)
    JobType.QWEN_TXT2IMG.value,
    JobType.QWEN_EDIT.value,
    JobType.IDENTITY_SWAP.value,
    JobType.WAN_T2V.value,
    JobType.WAN_ANIMATE.value,
    JobType.WAN_TI2V.value,
    JobType.WAN_I2V.value,
    JobType.ZIMAGE_TXT2IMG.value,
    JobType.ZIMAGE_TURBO_TXT2IMG.value,
]

ALLOWED_PROMPT_RUN_ENGINE_TYPES = [
    EngineType.SDXL.value,
    EngineType.UPSCALE.value,
    EngineType.KLING.value,
    EngineType.SORA.value,
    EngineType.NANOBANANA.value,
    EngineType.SEEDREAM.value,
    EngineType.GROK.value,
    EngineType.TOPAZ.value,
    EngineType.FLUX.value,
    EngineType.QWEN.value,
    EngineType.WAN.value,
    EngineType.ZIMAGE.value,
]

# RPC function names
RPC_SET_TOTP_SECRET = "rpc_set_user_totp_secret"
RPC_GET_TOTP_SECRET = "rpc_get_user_totp_secret"
RPC_UPSERT_PLATFORM_TOKENS = "rpc_upsert_platform_tokens"
RPC_GET_PLATFORM_TOKENS = "rpc_get_platform_tokens"
RPC_CREATE_WEBHOOK_ENDPOINT = "rpc_create_webhook_endpoint"
RPC_SET_COLLECTION_ITEM_PASSWORD = "rpc_set_collection_item_password"
RPC_GET_COLLECTION_ITEM_PASSWORD = "rpc_get_collection_item_password"
RPC_SET_ALBUM_ITEM_PASSWORD = "rpc_set_album_item_password"
RPC_GET_ALBUM_ITEM_PASSWORD = "rpc_get_album_item_password"
RPC_SET_HF_API_KEY_SECRET = "rpc_set_hf_api_key_secret"
RPC_GET_HF_API_KEY_SECRET = "rpc_get_hf_api_key_secret"
RPC_SET_CIVITAI_API_KEY_SECRET = "rpc_set_civitai_api_key_secret"
RPC_GET_CIVITAI_API_KEY_SECRET = "rpc_get_civitai_api_key_secret"
RPC_SET_ELEVENLABS_API_KEY_SECRET = "rpc_set_elevenlabs_api_key_secret"
RPC_GET_ELEVENLABS_API_KEY_SECRET = "rpc_get_elevenlabs_api_key_secret"
RPC_ASSIGN_CONNECTED_ACCOUNT_ORG = "assign_connected_account_org"
RPC_UNASSIGN_CONNECTED_ACCOUNT_ORG = "unassign_connected_account_org"
RPC_ADMIN_APPLY_CREDIT_ADJUSTMENT = "rpc_admin_apply_credit_adjustment"
RPC_CONSUME_REGISTRATION_CODE = "rpc_consume_registration_code"
RPC_RELEASE_REGISTRATION_CODE_USE = "rpc_release_registration_code_use"
RPC_CONSUME_REFERRAL_CODE = "rpc_consume_referral_code"
RPC_APPLY_REFERRAL_REWARD = "rpc_apply_referral_reward"
RPC_APPLY_BILLING_CREDIT_GRANT = "rpc_apply_billing_credit_grant"

# Table names (for clarity in repositories)
TABLE_USERS = "users"
TABLE_USER_SESSIONS = "user_sessions"
TABLE_ORGS = "organizations"
TABLE_MEMBERSHIPS = "organization_memberships"
TABLE_MODELS = "models"
TABLE_AVATARS = "avatar_profiles"
TABLE_MODEL_AVATARS = "avatars"
TABLE_PROMPT_TEMPLATES = "prompt_templates"
TABLE_PROMPT_TEMPLATE_EXAMPLE_OUTPUTS = "prompt_template_example_outputs"
TABLE_PROMPT_VERSIONS = "prompt_versions"
TABLE_PROMPT_RUNS = "prompt_runs"
TABLE_TEMPLATE_MODEL_LINKS = "prompt_template_model_links"
TABLE_PIPELINE_RUNS = "pipeline_runs"
TABLE_JOBS = "jobs"
TABLE_JOB_HISTORY = "job_status_history"
TABLE_ASSETS = "assets"
TABLE_ASSET_LINKS = "asset_model_links"
TABLE_ASSET_OUTPUTS = "asset_job_outputs"
TABLE_COLLECTIONS = "collections"
TABLE_COLLECTION_ITEMS = "collection_items"
TABLE_COLLECTION_ITEM_SECRETS = "collection_item_secrets"
TABLE_COLLECTION_MODEL_LINKS = "collection_model_links"
TABLE_ALBUMS = "albums"
TABLE_ALBUM_ITEMS = "album_items"
TABLE_ALBUM_ITEM_SECRETS = "album_item_secrets"
TABLE_ALBUM_MODEL_LINKS = "album_model_links"
TABLE_POSTS = "posts"
TABLE_ORG_POSTING_POLICIES = "org_posting_policies"
TABLE_ORG_DISCORD_WEBHOOKS = "org_discord_webhooks"
TABLE_ORG_DISCORD_WEBHOOK_EVENT_SUBSCRIPTIONS = "org_discord_webhook_event_subscriptions"
TABLE_WEBHOOK_EVENTS = "webhook_events"
TABLE_WEBHOOK_PROCESSING_LOGS = "webhook_processing_logs"
TABLE_RESOURCE_GRANTS = "resource_access_grants"
TABLE_WORKERS = "workers"
TABLE_CONNECTED_ACCOUNTS = "connected_accounts"
TABLE_MESSAGES = "messages"
TABLE_CONVERSATIONS = "conversations"
TABLE_CONVERSATION_LOCKS = "conversation_locks"
TABLE_CONVERSATION_LOCK_REQUESTS = "conversation_lock_requests"
TABLE_REVENUE_EVENTS = "revenue_events"
TABLE_USAGE_RECORDS = "usage_records"
TABLE_USER_WALLETS = "user_credit_wallets"
TABLE_MODEL_POOLS = "model_usage_pools"
TABLE_MODEL_POOL_MEMBERS = "model_usage_pool_members"
TABLE_POST_MEDIA = "post_media"
TABLE_POST_TARGETS = "post_targets"
TABLE_SCHEDULE_PLATFORMS = "schedule_platforms"
TABLE_SCHEDULE_CONTENT_TYPES = "schedule_content_types"
TABLE_SCHEDULE_ENTRIES = "schedule_entries"
TABLE_SCHEDULE_ENTRY_ASSETS = "schedule_entry_assets"
TABLE_CALENDAR_SUBSCRIPTIONS = "calendar_subscriptions"
TABLE_MODEL_PLATFORM_IDENTITIES = "model_platform_identities"
TABLE_HF_API_KEYS = "hf_api_keys"
TABLE_HF_API_KEY_SECRETS = "hf_api_key_secrets"
TABLE_CIVITAI_API_KEYS = "civitai_api_keys"
TABLE_CIVITAI_API_KEY_SECRETS = "civitai_api_key_secrets"
TABLE_ELEVENLABS_API_KEYS = "elevenlabs_api_keys"
TABLE_ELEVENLABS_API_KEY_SECRETS = "elevenlabs_api_key_secrets"
TABLE_ELEVENLABS_MODEL_VOICES = "elevenlabs_model_voices"
TABLE_SAVED_LORAS = "saved_loras"
TABLE_INTERNAL_NOTIFICATIONS = "internal_notifications"
TABLE_INTERNAL_NOTIFICATION_READS = "internal_notification_reads"
TABLE_AUDIT_LOGS = "audit_logs"
TABLE_WEBHOOK_ENDPOINTS = "webhook_endpoints"
TABLE_TIKTOK_VIDEOS = "tiktok_videos"
TABLE_TIKTOK_VIDEO_JOB_LINKS = "tiktok_video_job_links"
TABLE_TIKTOK_ACCOUNT_DAILY_ANALYTICS = "tiktok_account_daily_analytics"
TABLE_MODEL_DATASET_IMAGES = "model_dataset_images"
TABLE_LORA_ARTIFACTS = "lora_artifacts"
TABLE_MODEL_JOBS = "model_jobs"
TABLE_MODEL_CANDIDATES = "model_candidates"
TABLE_AVATAR_IMAGES = "avatar_images"
TABLE_CHARACTER_CREATIONS = "character_creations"
TABLE_ADMIN_FINANCE_ENTRIES = "admin_finance_entries"
TABLE_ADMIN_CREDIT_ADJUSTMENTS = "admin_credit_adjustments"
TABLE_APPLICATIONS = "applications"
TABLE_APPLICATION_VERSIONS = "application_versions"
TABLE_APPLICATION_DOWNLOADS = "application_downloads"
TABLE_APPLICATION_ACCESS = "application_access"
TABLE_CONTENT_DOWNLOAD_PROVIDER_SETTINGS = "content_download_provider_settings"
TABLE_CONTENT_DOWNLOAD_REQUESTS = "content_download_requests"
TABLE_CONTENT_DOWNLOAD_REQUEST_HISTORY = "content_download_request_history"
TABLE_CONTENT_DOWNLOAD_REQUEST_OUTPUTS = "content_download_request_outputs"
TABLE_REGISTRATION_SETTINGS = "registration_settings"
TABLE_REGISTRATION_CODES = "registration_codes"
TABLE_REFERRAL_PROGRAM_SETTINGS = "referral_program_settings"
TABLE_REFERRAL_CODES = "referral_codes"
TABLE_REFERRAL_ATTRIBUTIONS = "referral_attributions"
TABLE_REFERRAL_REWARDS = "referral_rewards"
TABLE_BILLING_CUSTOMERS = "billing_customers"
TABLE_BILLING_SUBSCRIPTIONS = "billing_subscriptions"
TABLE_BILLING_ORDERS = "billing_orders"
TABLE_BILLING_CREDIT_GRANTS = "billing_credit_grants"
TABLE_STRIPE_WEBHOOK_EVENTS = "stripe_webhook_events"
TABLE_STRIPE_WEBHOOK_PROCESSING_LOGS = "stripe_webhook_processing_logs"
TABLE_BILLING_REFUND_REVIEWS = "billing_refund_reviews"
TABLE_BILLING_SUBSCRIPTION_TYPE_LIMITS = "billing_subscription_type_limits"
TABLE_JOB_PERMISSION_OVERRIDES = "job_permission_overrides"
TABLE_WORKFLOWS = "workflows"
TABLE_WORKFLOW_RUNS = "workflow_runs"
TABLE_WORKFLOW_RUN_STEPS = "workflow_run_steps"
TABLE_WORKFLOW_BATCH_RUNS = "workflow_batch_runs"
TABLE_SCHEDULE_RECURRING_RULES = "schedule_recurring_rules"
TABLE_PUSH_NOTIFICATION_SUBSCRIPTIONS = "push_notification_subscriptions"
TABLE_CAPTION_PROJECTS = "caption_projects"
TABLE_TRANSCRIPTION_REQUESTS = "transcription_requests"
TABLE_TRANSCRIPTION_REQUEST_HISTORY = "transcription_request_history"
TABLE_CAPTION_RENDER_REQUESTS = "caption_render_requests"
TABLE_CAPTION_RENDER_REQUEST_HISTORY = "caption_render_request_history"
TABLE_CAPTION_TEMPLATES = "caption_templates"
TABLE_USER_CAPTION_TEMPLATES = "user_caption_templates"
TABLE_PRIVATE_CONTENT_PROVIDERS = "private_content_providers"
TABLE_PRIVATE_CONTENT_USER_ACCESS = "private_content_user_access"
TABLE_PRIVATE_CONTENT_TEMPLATES = "private_content_templates"
TABLE_PRIVATE_CONTENT_COLLECTIONS = "private_content_collections"
TABLE_PRIVATE_CONTENT_TEMPLATE_FAVOURITES = "private_content_template_favourites"

# S3 prefixes
S3_PREFIX_PRIVATE_CONTENT = "private-content"

# Platform names
PLATFORM_FANVUE = "fanvue"
PLATFORM_TIKTOK = "tiktok"

# Queue names
QUEUE_JOBS = "jobs"
QUEUE_MODEL_JOBS = "model_jobs"
QUEUE_ASSET_UPLOADS = "asset_uploads"
QUEUE_ASSET_DELETIONS = "asset_deletions"
QUEUE_CONTENT_DOWNLOAD_REQUESTS = "content_download_requests"
QUEUE_JOB_STATUS_SYNC = "job_status_sync"
QUEUE_SCHEDULE_EVENTS = "schedule_events"
QUEUE_TRANSCRIPTION_REQUESTS = "transcription_requests"
QUEUE_CAPTION_RENDERS = "caption_renders"
