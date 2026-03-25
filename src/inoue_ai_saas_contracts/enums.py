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
    KLING_3_0_MOTION_V2V = "kling_3_0_motion_v2v"
    KLING_AVATAR_STANDARD = "kling_avatar_standard"
    KLING_AVATAR_PRO = "kling_avatar_pro"
    SORA2_WATERMARK_REMOVE = "sora2_watermark_remove"
    SORA2_PRO_STORYBOARD = "sora2_pro_storyboard"
    WAN_2_6_T2V = "wan_2_6_t2v"
    WAN_2_6_I2V = "wan_2_6_i2v"
    WAN_2_6_V2V = "wan_2_6_v2v"


DEPRECATED_JOB_TYPES: frozenset[str] = frozenset(
    {
        "sdxl_image",
        "upscale",
        "hyperlora_sdxl_train",
        "lora_sdxl_dreambooth_train",
        "lora_qwen_image_train",
        "fanvue_upload",
        "fanvue_send_message",
        "fanvue_post",
        "identity_swap",
        "qwen_txt2img",
        "qwen_edit",
        "wan_t2v",
        "wan_animate",
        "wan_ti2v",
        "wan_i2v",
        "zimage_txt2img",
        "zimage_turbo_txt2img",
    }
)


JOB_TYPE_TITLES: dict[str, str] = {
    JobType.FACE_SWAP.value: "Face Swap",
    JobType.IMAGE_CROP.value: "Image Crop",
    JobType.THREADS_POST.value: "Threads · Post",
    JobType.SEEDREAM_V4_T2I.value: "Seedream V4 · Text to Image",
    JobType.SEEDREAM_V4_EDIT.value: "Seedream V4 · Edit",
    JobType.SEEDREAM_V4_5_T2I.value: "Seedream V4.5 · Text to Image",
    JobType.SEEDREAM_V4_5_EDIT.value: "Seedream V4.5 · Edit",
    JobType.SEEDREAM_5_LITE_T2I.value: "Seedream 5.0 Lite · Text to Image",
    JobType.SEEDREAM_5_LITE_I2I.value: "Seedream 5.0 Lite · Image to Image",
    JobType.NANOBANANA_T2I.value: "Nano Banana · Text to Image",
    JobType.NANOBANANA_I2I.value: "Nano Banana · Image to Image",
    JobType.NANOBANANA_PRO_T2I_1K2K.value: "Nano Banana Pro · Text to Image (1K/2K)",
    JobType.NANOBANANA_PRO_T2I_4K.value: "Nano Banana Pro · Text to Image (4K)",
    JobType.NANOBANANA_PRO_I2I_1K2K.value: "Nano Banana Pro · Image to Image (1K/2K)",
    JobType.NANOBANANA_PRO_I2I_4K.value: "Nano Banana Pro · Image to Image (4K)",
    JobType.NANOBANANA2_T2I_1K.value: "Nano Banana 2 · Text to Image (1K)",
    JobType.NANOBANANA2_T2I_2K.value: "Nano Banana 2 · Text to Image (2K)",
    JobType.NANOBANANA2_T2I_4K.value: "Nano Banana 2 · Text to Image (4K)",
    JobType.NANOBANANA2_I2I_1K.value: "Nano Banana 2 · Image to Image (1K)",
    JobType.NANOBANANA2_I2I_2K.value: "Nano Banana 2 · Image to Image (2K)",
    JobType.NANOBANANA2_I2I_4K.value: "Nano Banana 2 · Image to Image (4K)",
    JobType.SORA2_T2V.value: "Sora 2 · Text to Video",
    JobType.SORA2_I2V.value: "Sora 2 · Image to Video",
    JobType.SORA2PRO_T2V.value: "Sora 2 Pro · Text to Video",
    JobType.SORA2PRO_I2V.value: "Sora 2 Pro · Image to Video",
    JobType.KLING_O1_T2V.value: "Kling O1 · Text to Video",
    JobType.KLING_O1_I2V.value: "Kling O1 · Image to Video",
    JobType.KLING_2_6_T2V.value: "Kling 2.6 · Text to Video",
    JobType.KLING_2_6_I2V.value: "Kling 2.6 · Image to Video",
    JobType.KLING_2_6_MOTION_V2V.value: "Kling 2.6 Motion V2V",
    JobType.KLING_2_5_TURBO_T2V.value: "Kling 2.5 Turbo · Text to Video",
    JobType.KLING_2_5_TURBO_I2V.value: "Kling 2.5 Turbo · Image to Video",
    JobType.KLING_2_1_MASTER_T2V.value: "Kling 2.1 Master · Text to Video",
    JobType.KLING_2_1_MASTER_I2V.value: "Kling 2.1 Master · Image to Video",
    JobType.KLING_2_1_T2V.value: "Kling 2.1 · Text to Video",
    JobType.KLING_2_1_I2V.value: "Kling 2.1 · Image to Video",
    JobType.KLING_2_0_T2V.value: "Kling 2.0 · Text to Video",
    JobType.KLING_2_0_I2V.value: "Kling 2.0 · Image to Video",
    JobType.KLING_3_0_VIDEO.value: "Kling 3.0 Video",
    JobType.GROK_IMAGINE_TEXT_TO_VIDEO.value: "Grok · Text to Video",
    JobType.GROK_IMAGINE_IMAGE_TO_VIDEO.value: "Grok · Image to Video",
    JobType.GROK_IMAGINE_IMAGE_TO_IMAGE.value: "Grok · Image to Image",
    JobType.GROK_IMAGINE_TEXT_TO_IMAGE.value: "Grok · Text to Image",
    JobType.TOPAZ_IMAGE_UPSCALE.value: "Topaz · Image Upscale",
    JobType.TOPAZ_VIDEO_UPSCALE.value: "Topaz · Video Upscale",
    JobType.FLUX2_PRO_T2I.value: "Flux 2 Pro · Text to Image",
    JobType.FLUX2_PRO_I2I.value: "Flux 2 Pro · Image to Image",
    JobType.FLUX2_FLEX_T2I.value: "Flux 2 Flex · Text to Image",
    JobType.FLUX2_FLEX_I2I.value: "Flux 2 Flex · Image to Image",
    JobType.MOTIONMUSE_GENERATE.value: "MotionMuse · Generate",
    JobType.KLING_3_0_MOTION_V2V.value: "Kling 3.0 · Motion Control",
    JobType.KLING_AVATAR_STANDARD.value: "Kling · AI Avatar Standard",
    JobType.KLING_AVATAR_PRO.value: "Kling · AI Avatar Pro",
    JobType.SORA2_WATERMARK_REMOVE.value: "Sora 2 · Watermark Remover",
    JobType.SORA2_PRO_STORYBOARD.value: "Sora 2 Pro · Storyboard",
    JobType.WAN_2_6_T2V.value: "Wan 2.6 · Text to Video",
    JobType.WAN_2_6_I2V.value: "Wan 2.6 · Image to Video",
    JobType.WAN_2_6_V2V.value: "Wan 2.6 · Video to Video",
}


def job_type_title(job_type: str) -> str:
    """Resolve a human-friendly title for a job type from the canonical map."""
    if job_type in JOB_TYPE_TITLES:
        return JOB_TYPE_TITLES[job_type]
    return " ".join(word.capitalize() for word in job_type.replace("_", " ").split())


class ModelCreationMode(str, Enum):
    PHOTO_LORA = "photo_lora"
    BASE_TRAITS = "base_traits"
    UPLOADED_LORA = "uploaded_lora"
    HUGGINGFACE_LORA = "huggingface_lora"


DEPRECATED_MODEL_CREATION_MODES: frozenset[str] = frozenset(
    {
        ModelCreationMode.PHOTO_LORA.value,
        ModelCreationMode.UPLOADED_LORA.value,
        ModelCreationMode.HUGGINGFACE_LORA.value,
    }
)


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


DEPRECATED_ENGINE_TYPES: frozenset[str] = frozenset(
    {
        EngineType.SDXL.value,
        EngineType.UPSCALE.value,
        EngineType.LORA.value,
        EngineType.QWEN.value,
        EngineType.ZIMAGE.value,
    }
)


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


class IdentityAssetRole(str, Enum):
    FACE = "face"
    BODY = "body"
    STYLE = "style"
    GENERAL = "general"
