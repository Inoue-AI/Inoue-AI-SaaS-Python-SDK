from __future__ import annotations

from pydantic import BaseModel


class WebhookEndpointCreateResult(BaseModel):
    endpoint_id: str


class WebhookIngestResult(BaseModel):
    stored_event_id: str
