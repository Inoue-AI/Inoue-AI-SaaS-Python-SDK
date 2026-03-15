from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .enums import ErrorCode

ERROR_CATALOG: dict[ErrorCode, str] = {
    ErrorCode.BAD_REQUEST: "Bad request",
    ErrorCode.UNAUTHORIZED: "Unauthorized",
    ErrorCode.FORBIDDEN: "Forbidden",
    ErrorCode.NOT_FOUND: "Not found",
    ErrorCode.CONFLICT: "Conflict",
    ErrorCode.VALIDATION_ERROR: "Validation error",
    ErrorCode.INTERNAL_ERROR: "Internal error",
    ErrorCode.POSTGREST_ERROR: "PostgREST error",
    ErrorCode.CONSTRAINT_VIOLATION: "Constraint violation",
}


class ApiException(Exception):
    def __init__(self, code: ErrorCode, http_status: int, message: str | None = None, details: Any | None = None):
        super().__init__(message or ERROR_CATALOG.get(code, "Error"))
        self.code = code
        self.http_status = http_status
        self.message = message or ERROR_CATALOG.get(code, "Error")
        self.details = details


class ErrorDetail(BaseModel):
    code: ErrorCode | str
    message: str
    details: Any | None = None
