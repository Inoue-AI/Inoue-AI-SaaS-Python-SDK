from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditLog(BaseModel):
    id: str
    org_id: str | None = None
    actor_user_id: str
    actor_email: str | None = None
    action_type: str
    resource_type: str
    resource_id: str | None = None
    context_json: dict[str, Any] | None = None
    created_at: datetime | None = None
