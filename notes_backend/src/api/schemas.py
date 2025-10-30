from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base fields for a note, used by create and update operations."""

    title: Optional[str] = Field(default=None, description="Title of the note")
    content: Optional[str] = Field(default=None, description="Content of the note")


class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


class NoteUpdate(NoteBase):
    """Schema for updating an existing note."""
    pass


class NoteOut(NoteBase):
    """Schema representing a note returned by the API."""

    id: int = Field(..., description="Unique identifier of the note")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")

    class Config:
        from_attributes = True
