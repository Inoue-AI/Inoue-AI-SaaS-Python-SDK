from __future__ import annotations

from typing import Any

from inoue_ai_saas_contracts import ErrorCode


class SdkError(Exception):
    def __init__(
        self,
        code: ErrorCode | str,
        message: str,
        http_status: int,
        trace_id: str | None = None,
        details: Any | None = None,
        response: Any | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.http_status = http_status
        self.trace_id = trace_id
        self.details = details
        self.response = response

    def __str__(self) -> str:  # pragma: no cover - formatting only
        suffix = f"status={self.http_status}"
        if self.trace_id:
            suffix = f"trace_id={self.trace_id}, {suffix}"
        return f"{self.code}: {self.message} ({suffix})"


class SdkTransportError(Exception):
    def __init__(
        self, message: str, trace_id: str | None = None, http_status: int | None = None, details: Any | None = None
    ):
        super().__init__(message)
        self.trace_id = trace_id
        self.http_status = http_status
        self.details = details

    def __str__(self) -> str:  # pragma: no cover - formatting only
        suffix = []
        if self.trace_id:
            suffix.append(f"trace_id={self.trace_id}")
        if self.http_status is not None:
            suffix.append(f"status={self.http_status}")
        suffix_text = f" ({', '.join(suffix)})" if suffix else ""
        return f"{self.args[0]}{suffix_text}"
