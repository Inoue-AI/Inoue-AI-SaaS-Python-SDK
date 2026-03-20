from __future__ import annotations

from enum import Enum


class ErrorCode(str, Enum):
    BAD_REQUEST = "bad_request"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    VALIDATION_ERROR = "validation_error"
    INTERNAL_ERROR = "internal_error"
    POSTGREST_ERROR = "postgrest_error"
    CONSTRAINT_VIOLATION = "constraint_violation"


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"


class PipelineStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"


class PromptRunStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"


class JobType(str, Enum):
    SDXL_IMAGE = "sdxl_image"
    UPSCALE = "upscale"
    HYPERLORA_SDXL_TRAIN = "hyperlora_sdxl_train"
    LORA_SDXL_DB_TRAIN = "lora_sdxl_dreambooth_train"
    LORA_QWEN_IMAGE_TRAIN = "lora_qwen_image_train"
    FACE_SWAP = "face_swap"
    IMAGE_CROP = "image_crop"
    FANVUE_UPLOAD = "fanvue_upload"
    FANVUE_SEND_MESSAGE = "fanvue_send_message"
    FANVUE_POST = "fanvue_post"
    THREADS_POST = "threads_post"
    SEEDREAM_V4_T2I = "seedream_v4_t2i"
    SEEDREAM_V4_EDIT = "seedream_v4_edit"
    SEEDREAM_V4_5_T2I = "seedream_v4_5_t2i"
    SEEDREAM_V4_5_EDIT = "seedream_v4_5_edit"
    NANOBANANA_T2I = "nanobanana_t2i"
    NANOBANANA_I2I = "nanobanana_i2i"
    NANOBANANA_PRO_T2I_1K2K = "nanobanana_pro_t2i_1k2k"
    NANOBANANA_PRO_T2I_4K = "nanobanana_pro_t2i_4k"
    NANOBANANA_PRO_I2I_1K2K = "nanobanana_pro_i2i_1k2k"
    NANOBANANA_PRO_I2I_4K = "nanobanana_pro_i2i_4k"
    NANOBANANA2_T2I_1K = "nanobanana2_t2i_1k"
    NANOBANANA2_T2I_2K = "nanobanana2_t2i_2k"
    NANOBANANA2_T2I_4K = "nanobanana2_t2i_4k"
    NANOBANANA2_I2I_1K = "nanobanana2_i2i_1k"
    NANOBANANA2_I2I_2K = "nanobanana2_i2i_2k"
    NANOBANANA2_I2I_4K = "nanobanana2_i2i_4k"
    SORA2_T2V = "sora2_t2v"
    SORA2_I2V = "sora2_i2v"
    SORA2PRO_T2V = "sora2pro_t2v"
    SORA2PRO_I2V = "sora2pro_i2v"
    KLING_O1_T2V = "kling_o1_t2v"
    KLING_O1_I2V = "kling_o1_i2v"
    KLING_2_6_T2V = "kling_2_6_t2v"
    KLING_2_6_I2V = "kling_2_6_i2v"
    KLING_2_6_MOTION_V2V = "kling_2_6_motion_v2v"
    KLING_2_5_TURBO_T2V = "kling_2_5_turbo_t2v"
    KLING_2_5_TURBO_I2V = "kling_2_5_turbo_i2v"
    KLING_2_1_MASTER_T2V = "kling_2_1_master_t2v"
    KLING_2_1_MASTER_I2V = "kling_2_1_master_i2v"
    KLING_2_1_T2V = "kling_2_1_t2v"
    KLING_2_1_I2V = "kling_2_1_i2v"
    KLING_2_0_T2V = "kling_2_0_t2v"
    KLING_2_0_I2V = "kling_2_0_i2v"
    KLING_3_0_VIDEO = "kling_3_0_video"
    GROK_IMAGINE_TEXT_TO_VIDEO = "grok_imagine_text_to_video"
    GROK_IMAGINE_IMAGE_TO_VIDEO = "grok_imagine_image_to_video"
    GROK_IMAGINE_IMAGE_TO_IMAGE = "grok_imagine_image_to_image"
    GROK_IMAGINE_TEXT_TO_IMAGE = "grok_imagine_text_to_image"
    TOPAZ_IMAGE_UPSCALE = "topaz_image_upscale"
    TOPAZ_VIDEO_UPSCALE = "topaz_video_upscale"
    SEEDREAM_5_LITE_T2I = "seedream_5_lite_t2i"
    SEEDREAM_5_LITE_I2I = "seedream_5_lite_i2i"
    FLUX2_PRO_T2I = "flux2_pro_t2i"
    FLUX2_PRO_I2I = "flux2_pro_i2i"
    FLUX2_FLEX_T2I = "flux2_flex_t2i"
    FLUX2_FLEX_I2I = "flux2_flex_i2i"
    QWEN_TXT2IMG = "qwen_txt2img"
    QWEN_EDIT = "qwen_edit"
    IDENTITY_SWAP = "identity_swap"
    WAN_T2V = "wan_t2v"
    WAN_ANIMATE = "wan_animate"
    WAN_TI2V = "wan_ti2v"
    WAN_I2V = "wan_i2v"
    ZIMAGE_TXT2IMG = "zimage_txt2img"
    ZIMAGE_TURBO_TXT2IMG = "zimage_turbo_txt2img"
    MOTIONMUSE_GENERATE = "motionmuse_generate"


class ModelCreationMode(str, Enum):
    PHOTO_LORA = "photo_lora"
    BASE_TRAITS = "base_traits"
    UPLOADED_LORA = "uploaded_lora"
    HUGGINGFACE_LORA = "huggingface_lora"


class ModelWorkflowStatus(str, Enum):
    DRAFT = "draft"
    DATASET_READY = "dataset_ready"
    TRAINING_QUEUED = "training_queued"
    TRAINING_RUNNING = "training_running"
    TRAINING_FAILED = "training_failed"
    READY = "ready"
    ACTIVE = "active"
    ARCHIVED = "archived"


class ModelJobType(str, Enum):
    HYPERLORA_SDXL_TRAIN = "hyperlora_sdxl_train"
    LORA_SDXL_DB_TRAIN = "lora_sdxl_dreambooth_train"
    LORA_QWEN_IMAGE_TRAIN = "lora_qwen_image_train"


class OrgRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class GranteeType(str, Enum):
    USER = "user"
    ORG = "org"


class ResourceType(str, Enum):
    MODEL = "model"
    COLLECTION = "collection"
    ALBUM = "album"


class AccessLevel(str, Enum):
    VIEW = "view"
    EDIT = "edit"
    EDITOR = "editor"


class MembershipStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class PostStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    PUBLISHED = "published"
    CANCELED = "canceled"
    FAILED = "failed"


class PostTargetStatus(str, Enum):
    PENDING = "pending"
    PUBLISHED = "published"
    FAILED = "failed"


class ScheduleStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELED = "canceled"


class ScheduleEventType(str, Enum):
    SCHEDULE_POST = "schedule_post"
    REMINDER = "reminder"


class RecurrenceFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class AssetType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"
    AUDIO = "audio"
    OTHER = "other"


class EngineType(str, Enum):
    SDXL = "sdxl"
    KLING = "kling"
    SORA = "sora"
    UPSCALE = "realesrgan"
    LORA = "lora_train"
    NANOBANANA = "nanobanana"
    SEEDREAM = "seedream"
    GROK = "grok"
    TOPAZ = "topaz"
    FLUX = "flux"
    QWEN = "qwen"
    WAN = "wan"
    ZIMAGE = "zimage"
    MOTIONMUSE = "motionmuse"


class EngineCategory(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    WORKFLOW = "workflow"


class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class WorkflowRunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    AWAITING_CLIENT = "awaiting_client"
    AWAITING_INPUT = "awaiting_input"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
