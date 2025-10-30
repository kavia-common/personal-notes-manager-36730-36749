from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from api.db import get_db, Base, engine
from api.models import Note
from api.schemas import NoteCreate, NoteUpdate, NoteOut

router = APIRouter()

# Ensure tables are created on import if not existing
Base.metadata.create_all(bind=engine)


def _get_note_or_404(db: Session, note_id: int) -> Note:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create Note",
    description="Create a new note. Title and content are optional.",
)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteOut:
    """
    Create a new note with optional title and content.

    Parameters:
        payload: NoteCreate - The note data to create.
        db: Session - Injected database session.

    Returns:
        NoteOut: The created note with its ID and timestamps.
    """
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[NoteOut],
    summary="List Notes",
    description="Retrieve a list of all notes.",
)
def list_notes(db: Session = Depends(get_db)) -> List[NoteOut]:
    """
    List all notes.

    Parameters:
        db: Session - Injected database session.

    Returns:
        List[NoteOut]: All notes in the database.
    """
    return db.query(Note).order_by(Note.created_at.desc()).all()


# PUBLIC_INTERFACE
@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get Note",
    description="Retrieve a single note by its ID.",
)
def get_note(
    note_id: int = Path(..., description="ID of the note to retrieve", ge=1),
    db: Session = Depends(get_db),
) -> NoteOut:
    """
    Get a specific note by ID.

    Parameters:
        note_id: int - The ID of the note to fetch.
        db: Session - Injected database session.

    Returns:
        NoteOut: The requested note.
    """
    note = _get_note_or_404(db, note_id)
    return note


# PUBLIC_INTERFACE
@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update Note",
    description="Update a note's title and/or content.",
)
def update_note(
    payload: NoteUpdate,
    note_id: int = Path(..., description="ID of the note to update", ge=1),
    db: Session = Depends(get_db),
) -> NoteOut:
    """
    Update a specific note by ID.

    Parameters:
        payload: NoteUpdate - Fields to update.
        note_id: int - The ID of the note to update.
        db: Session - Injected database session.

    Returns:
        NoteOut: The updated note.
    """
    note = _get_note_or_404(db, note_id)

    # Apply updates if provided
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content

    # Update the timestamp manually for SQLite compatibility
    note.updated_at = datetime.utcnow()

    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Note",
    description="Delete a note by its ID.",
)
def delete_note(
    note_id: int = Path(..., description="ID of the note to delete", ge=1),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a specific note by ID.

    Parameters:
        note_id: int - The ID of the note to delete.
        db: Session - Injected database session.

    Returns:
        None
    """
    note = _get_note_or_404(db, note_id)
    db.delete(note)
    db.commit()
    return None
