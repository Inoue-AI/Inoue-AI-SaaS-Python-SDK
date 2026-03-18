# Inoue AI SaaS Python SDK

**Canonical Python SDK** for the Inoue AI SaaS API. This is the single source of truth for the SDK client and shared contracts used across the Inoue AI ecosystem.

Contracts originate in the backend repo (`Inoue-AI-SaaS-Backend/packages/contracts/`) and are synced here automatically via CI.

## Installation

```bash
pip install inoue-ai-saas-sdk @ git+https://github.com/Inoue-AI/Inoue-AI-SaaS-Python-SDK.git@main
```

## Packages

This repository provides two importable packages:

- **`inoue_ai_saas_contracts`** — Pydantic models, enums, and constants shared across the Inoue AI ecosystem (Backend API, Worker Orchestrator, Download Worker, etc.)
- **`inoue_ai_saas_sdk`** — Async HTTP client for the Inoue AI SaaS API

## Quick Start

```python
from inoue_ai_saas_sdk import InoueAiSaasClient

async with InoueAiSaasClient("https://api.inoue.ai", access_token="...") as client:
    result = await client.system.health()
    print(result.data)
```

### Using contracts directly (e.g. in workers)

```python
from inoue_ai_saas_contracts import JobType, JobStatus
from inoue_ai_saas_contracts.constants import QUEUE_JOBS

# Type-safe job type checking
if job_type == JobType.SDXL_IMAGE.value:
    ...
```

## Requirements

- Python >= 3.11
- httpx >= 0.27.0
- pydantic >= 2.6
