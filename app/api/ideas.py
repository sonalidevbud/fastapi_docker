from datetime import datetime, time, timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import argon2
from sqlalchemy import func
from sqlmodel import Session, select

from app.config import get_settings
from app.db import get_session
from app.models.models import (
    Files,
    IdeaAddIn,
    IdeaIndexResponse,
    Ideas,
    StandardResponse,
)
from app.service.bearer_auth import has_token
from app.service.helpers import get_uuid
from app.service.password import Password

idea_router = APIRouter()


@idea_router.get("/", response_model=List[IdeaIndexResponse], name="ideas:List")
async def ideas_get_all(*, session: Session = Depends(get_session), auth=Depends(has_token)):
    ideas = session.exec(
        select(Ideas).where(Ideas.account_id == auth["account"]).where(Ideas.deleted_at.is_(None))
    ).all()

    return ideas


@idea_router.get("/{idea_uuid}", response_model=IdeaIndexResponse, name="ideas:Item")
async def ideas_get_one(*, session: Session = Depends(get_session), idea_uuid: UUID, auth=Depends(has_token)):
    idea = session.exec(
        select(Ideas)
        .where(Ideas.account_id == auth["account"])
        .where(Ideas.uuid == idea_uuid)
        .where(Ideas.deleted_at.is_(None))
    ).one_or_none()

    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    return idea


@idea_router.post("/", response_model=StandardResponse, name="idea:Add")
async def user_get_all(*, session: Session = Depends(get_session), idea: IdeaAddIn, auth=Depends(has_token)):

    res = IdeaAddIn.from_orm(idea)

    files = []
    if res.files is not None:
        for file in res.files:
            db_file = session.exec(
                select(Files).where(Files.uuid == file).where(Files.deleted_at.is_(None))
            ).one_or_none()
            if db_file:
                files.append(db_file)

    new_idea = Ideas(
        uuid=get_uuid(),
        account_id=auth["account"],
        author_id=auth["user"],
        color=res.color,
        title=res.title,
        description=res.description,
        files=files,
        created_at=datetime.utcnow(),
    )

    session.add(new_idea)
    session.commit()
    session.refresh(new_idea)

    return {"ok": True}


@idea_router.delete("/{idea_uuid}", response_model=StandardResponse, name="idea:Delete")
async def user_delete_one(*, session: Session = Depends(get_session), idea_uuid: UUID, auth=Depends(has_token)):

    db_idea = session.exec(
        select(Ideas).where(Ideas.account_id == auth["account"]).where(Ideas.uuid == idea_uuid)
    ).one_or_none()

    if not db_idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    # db_task.events.remove()

    # Delete Files
    for pictures in db_idea.pictures:
        db_file = session.exec(select(Files).where(Files.id == pictures.id)).one()
        db_idea.pictures.remove(pictures)
        session.delete(db_file)
        session.commit()

    session.delete(db_idea)
    session.commit()

    # update_package = {"deleted_at": datetime.utcnow()}  # soft delete
    # for key, value in update_package.items():
    #     setattr(db_task, key, value)

    # session.add(db_task)
    # session.commit()
    # session.refresh(db_task)

    return {"ok": True}
