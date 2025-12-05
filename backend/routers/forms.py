"""
Forms Router - Manage form configurations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from core.database import get_session
from models.schema_builder import FormSchema, FormSchemaCreate, FormSchemaUpdate, FormSchemaRead, App

router = APIRouter(prefix="/apps/{app_id}/forms", tags=["forms"])


@router.get("", response_model=List[FormSchemaRead])
def list_forms(
    app_id: int,
    session: Session = Depends(get_session)
):
    """List all forms for an app"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    statement = select(FormSchema).where(FormSchema.app_id == app_id)
    forms = session.exec(statement).all()
    return forms


@router.post("", response_model=FormSchemaRead, status_code=201)
def create_form(
    app_id: int,
    form: FormSchemaCreate,
    session: Session = Depends(get_session)
):
    """Create a new form"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    existing = session.exec(
        select(FormSchema).where(FormSchema.app_id == app_id, FormSchema.name == form.name)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Form with this name already exists")
    
    db_form = FormSchema(**form.model_dump(), app_id=app_id)
    session.add(db_form)
    session.commit()
    session.refresh(db_form)
    return db_form


@router.get("/{form_id}", response_model=FormSchemaRead)
def get_form(
    app_id: int,
    form_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific form"""
    form = session.get(FormSchema, form_id)
    if not form or form.app_id != app_id:
        raise HTTPException(status_code=404, detail="Form not found")
    return form


@router.patch("/{form_id}", response_model=FormSchemaRead)
def update_form(
    app_id: int,
    form_id: int,
    form_update: FormSchemaUpdate,
    session: Session = Depends(get_session)
):
    """Update a form"""
    form = session.get(FormSchema, form_id)
    if not form or form.app_id != app_id:
        raise HTTPException(status_code=404, detail="Form not found")
    
    update_data = form_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(form, key, value)
    
    session.add(form)
    session.commit()
    session.refresh(form)
    return form


@router.delete("/{form_id}", status_code=204)
def delete_form(
    app_id: int,
    form_id: int,
    session: Session = Depends(get_session)
):
    """Delete a form"""
    form = session.get(FormSchema, form_id)
    if not form or form.app_id != app_id:
        raise HTTPException(status_code=404, detail="Form not found")
    
    session.delete(form)
    session.commit()
    return None
