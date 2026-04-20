from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.database import get_session
from app.models import Program, Project
from app.rate_limit import limiter
from app.schemas.core import (
    ProgrammeCreate,
    ProgrammeOut,
    ProgrammeWithProjects,
    ProjectCreate,
    ProjectOut,
)

router = APIRouter(prefix="/programmes", tags=["programmes"])
_write_limit = get_settings().rate_limit_write


@router.get("", response_model=list[ProgrammeOut])
async def list_programmes(session: AsyncSession = Depends(get_session)) -> list[Program]:
    result = await session.execute(select(Program).order_by(Program.id))
    return list(result.scalars().all())


@router.post("", response_model=ProgrammeOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(_write_limit)
async def create_programme(
    request: Request,
    payload: ProgrammeCreate,
    session: AsyncSession = Depends(get_session),
) -> Program:
    existing = await session.execute(select(Program).where(Program.code == payload.code))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Programme with code '{payload.code}' already exists",
        )
    programme = Program(**payload.model_dump())
    session.add(programme)
    await session.commit()
    await session.refresh(programme)
    return programme


@router.get("/{programme_id}", response_model=ProgrammeWithProjects)
async def get_programme(
    programme_id: int,
    session: AsyncSession = Depends(get_session),
) -> Program:
    stmt = (
        select(Program)
        .where(Program.id == programme_id)
        .options(selectinload(Program.projects))
    )
    result = await session.execute(stmt)
    programme = result.scalar_one_or_none()
    if programme is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Programme not found")
    return programme


@router.get("/{programme_id}/projects", response_model=list[ProjectOut])
async def list_programme_projects(
    programme_id: int,
    session: AsyncSession = Depends(get_session),
) -> list[Project]:
    result = await session.execute(
        select(Project).where(Project.program_id == programme_id).order_by(Project.id)
    )
    return list(result.scalars().all())


@router.post(
    "/{programme_id}/projects",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(_write_limit)
async def create_project(
    request: Request,
    programme_id: int,
    payload: ProjectCreate,
    session: AsyncSession = Depends(get_session),
) -> Project:
    programme = await session.get(Program, programme_id)
    if programme is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Programme not found",
        )
    data = payload.model_dump()
    data["program_id"] = programme_id
    project = Project(**data)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project
