from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class LegalDocumentSection(BaseModel):
    heading: str
    body: list[str]


class LegalDocumentResponse(BaseModel):
    key: str
    title: str
    version: str
    effective_date: date
    summary: str
    sections: list[LegalDocumentSection]
