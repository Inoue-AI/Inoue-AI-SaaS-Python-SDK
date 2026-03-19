"""Test fixtures for SDK tests."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from inoue_ai_saas_sdk import InoueAiSaasClient


class MockTransport(httpx.AsyncBaseTransport):
    """Captures outbound requests and returns a configurable JSON envelope."""

    def __init__(self, data: Any = None, status: int = 200, ok: bool = True):
        self._data = data
        self._status = status
        self._ok = ok
        self.last_request: httpx.Request | None = None

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        self.last_request = request
        body = json.dumps({
            "ok": self._ok,
            "data": self._data,
            "meta": {"trace_id": "test-trace", "request_id": "test-req"},
        }).encode()
        return httpx.Response(status_code=self._status, content=body, headers={"content-type": "application/json"})


@pytest.fixture()
def mock_transport():
    return MockTransport(data={})


@pytest.fixture()
def client(mock_transport: MockTransport) -> InoueAiSaasClient:
    return InoueAiSaasClient(
        "https://test.inoue.ai",
        access_token="test-token",
        transport=mock_transport,
        webhooks_transport=mock_transport,
    )
