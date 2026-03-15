from __future__ import annotations

from pydantic import BaseModel


class DeletionResult(BaseModel):
    deleted: bool


class ReadResult(BaseModel):
    read: bool


class UnreadResult(BaseModel):
    unread: bool


class MutedResult(BaseModel):
    muted: bool


class UnmutedResult(BaseModel):
    unmuted: bool


class AcceptedResult(BaseModel):
    accepted: bool


class DeclinedResult(BaseModel):
    declined: bool


class RevokedResult(BaseModel):
    revoked: bool


class ApprovedResult(BaseModel):
    approved: bool


class DeniedResult(BaseModel):
    denied: bool


class UnlockedResult(BaseModel):
    unlocked: bool


class DisconnectedResult(BaseModel):
    disconnected: bool


class BannedResult(BaseModel):
    banned: bool


class QuitResult(BaseModel):
    quit: bool
