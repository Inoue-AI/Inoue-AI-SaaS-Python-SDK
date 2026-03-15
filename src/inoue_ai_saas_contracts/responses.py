from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from .constants import API_VERSION
from .enums import ErrorCode

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int | None = None


class ResponseMeta(BaseModel):
    trace_id: str
    request_id: str | None = None
    pagination: PaginationMeta | None = None
    version: str = Field(default=API_VERSION)


class ErrorBody(BaseModel):
    code: ErrorCode | str
    message: str
    details: object | None = None


class SuccessResponse(BaseModel, Generic[T]):
    ok: bool = True
    data: T | None = None
    meta: ResponseMeta


class ErrorResponse(BaseModel):
    ok: bool = False
    error: ErrorBody
    meta: ResponseMeta
