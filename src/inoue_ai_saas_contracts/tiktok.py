"""TikTok integration contracts."""

from __future__ import annotations

import datetime as dt

from pydantic import BaseModel, Field

from .fanvue import ConnectedAccount
from .pagination import PaginationQuery


class TiktokAccountListQuery(PaginationQuery):
    ownership: str | None = None
    status: str | None = None


class TiktokConnectStartResponse(BaseModel):
    url: str
    state: str
    mode: str


class TiktokConnectCallbackPayload(BaseModel):
    code: str
    state: str | None = None


class TiktokTokenRefreshRequest(BaseModel):
    connected_account_id: str
    refresh_token: str


class TiktokTokenRefreshResponse(BaseModel):
    connected_account_id: str
    access_token: str
    refresh_token: str
    token_expires_at: dt.datetime


class TiktokConnectedAccount(ConnectedAccount):
    pass


class TiktokVideoJobLink(BaseModel):
    id: str
    job_id: str
    note: str | None = None
    linked_by_user_id: str | None = None
    linked_at: dt.datetime | None = None
    job_type: str | None = None
    job_status: str | None = None
    model_id: str | None = None


class TiktokVideo(BaseModel):
    id: str
    connected_account_id: str
    remote_video_id: str
    title: str | None = None
    description: str | None = None
    cover_url: str | None = None
    share_url: str | None = None
    duration_seconds: int | None = None
    published_at: dt.datetime | None = None
    view_count: int | None = None
    like_count: int | None = None
    comment_count: int | None = None
    share_count: int | None = None
    save_count: int | None = None
    watch_time_seconds: int | None = None
    model_id: str | None = None
    linked_jobs: list[TiktokVideoJobLink] = Field(default_factory=list)
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class TiktokVideoListQuery(PaginationQuery):
    model_id: str | None = None
    q: str | None = None


class TiktokVideoJobLinkRequest(BaseModel):
    connected_account_id: str
    job_id: str
    note: str | None = None


class TiktokAnalyticsPoint(BaseModel):
    date: str
    followers_count: int = 0
    following_count: int = 0
    views_count: int = 0
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    profile_views_count: int = 0
    video_views_count: int = 0
    engagement_rate: float = 0.0


class TiktokAnalyticsSummary(BaseModel):
    connected_account_id: str
    model_id: str | None = None
    followers_count: int = 0
    following_count: int = 0
    views_count: int = 0
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    profile_views_count: int = 0
    video_views_count: int = 0
    follower_growth: int = 0
    avg_daily_views: float = 0.0
    avg_engagement_rate: float = 0.0


class TiktokAnalyticsResponse(BaseModel):
    account: TiktokConnectedAccount
    summary: TiktokAnalyticsSummary
    series: list[TiktokAnalyticsPoint] = Field(default_factory=list)
    top_videos: list[TiktokVideo] = Field(default_factory=list)


class TiktokAnalyticsQuery(BaseModel):
    connected_account_id: str
    model_id: str | None = None
    days: int = 30
