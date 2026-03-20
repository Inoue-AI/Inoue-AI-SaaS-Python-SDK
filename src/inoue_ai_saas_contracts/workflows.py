"""Workflow builder contracts."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .pagination import PaginationQuery

# ── Workflow CRUD ──


class WorkflowCreateRequest(BaseModel):
    name: str
    description: str | None = None
    owner_org_id: str | None = None
    graph: dict = Field(default_factory=dict)
    status: str = "draft"
    tags: list[str] = Field(default_factory=list)


class WorkflowUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    graph: dict | None = None
    status: str | None = None
    tags: list[str] | None = None


class WorkflowListQuery(PaginationQuery):
    owner_org_id: str | None = None
    status: str | None = None
    search: str | None = None


class WorkflowResponse(BaseModel):
    """Maps to frontend WorkflowListItem."""

    id: str
    name: str
    description: str | None = None
    status: str
    owner_user_id: str | None = None
    owner_org_id: str | None = None
    version: int = 1
    tags: list[str] = Field(default_factory=list)
    engine_slugs: list[str] = Field(default_factory=list)
    run_count: int = 0
    last_run_at: str | None = None
    created_at: str
    updated_at: str


class WorkflowDetailResponse(WorkflowResponse):
    """Maps to frontend WorkflowDetail — includes the full graph."""

    graph: dict = Field(default_factory=dict)


# ── Workflow Runs ──


class WorkflowRunRequest(BaseModel):
    inputs: list[dict] = Field(default_factory=list)
    owner_org_id: str | None = None


class WorkflowBatchRunRequest(BaseModel):
    input_matrix: list[list[dict]] = Field(default_factory=list)
    owner_org_id: str | None = None


class WorkflowStepResolveRequest(BaseModel):
    """Body for POST /v1/workflows/run-steps/:id/resolve."""

    outputs: dict = Field(default_factory=dict)
    output_asset_ids: list[str] = Field(default_factory=list)


class WorkflowRunStepResponse(BaseModel):
    id: str
    node_id: str
    node_label: str
    engine_slug: str | None = None
    job_type: str | None = None
    status: str
    job_id: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    inputs: dict = Field(default_factory=dict)
    outputs: dict = Field(default_factory=dict)
    output_asset_ids: list[str] = Field(default_factory=list)
    error: str | None = None


class WorkflowRunResponse(BaseModel):
    id: str
    workflow_id: str
    workflow_name: str | None = None
    status: str
    inputs: list[dict] = Field(default_factory=list)
    steps: list[WorkflowRunStepResponse] = Field(default_factory=list)
    batch_index: int | None = None
    batch_total: int | None = None
    created_at: str
    updated_at: str
    finished_at: str | None = None
    error: str | None = None
    total_cost: float | None = None


class WorkflowBatchRunResponse(BaseModel):
    id: str
    workflow_id: str
    status: str
    input_matrix: list[list[dict]] = Field(default_factory=list)
    runs: list[WorkflowRunResponse] = Field(default_factory=list)
    created_at: str
    updated_at: str


# ── Approval Gate ──


class ApprovalGateApproveRequest(BaseModel):
    """Body for POST /v1/workflow-runs/run-steps/:id/approve."""

    pass


class ApprovalGateRejectRequest(BaseModel):
    """Body for POST /v1/workflow-runs/run-steps/:id/reject."""

    reason: str | None = None


class StepInputsUpdateRequest(BaseModel):
    """Body for PATCH /v1/workflow-runs/run-steps/:id/inputs."""

    inputs: dict = Field(default_factory=dict)
