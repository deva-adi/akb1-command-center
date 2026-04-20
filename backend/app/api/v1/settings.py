from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.models import AppSetting
from app.rate_limit import limiter
from app.schemas.settings import AppSettingOut, AppSettingUpdate

router = APIRouter(prefix="/settings", tags=["settings"])
_write_limit = get_settings().rate_limit_write


@router.get("", response_model=list[AppSettingOut])
async def list_settings(session: AsyncSession = Depends(get_session)) -> list[AppSetting]:
    result = await session.execute(select(AppSetting).order_by(AppSetting.key))
    return list(result.scalars().all())


@router.get("/{key}", response_model=AppSettingOut)
async def get_setting(key: str, session: AsyncSession = Depends(get_session)) -> AppSetting:
    setting = await session.get(AppSetting, key)
    if setting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Setting '{key}' not found"
        )
    return setting


@router.put("/{key}", response_model=AppSettingOut)
@limiter.limit(_write_limit)
async def update_setting(
    request: Request,
    key: str,
    payload: AppSettingUpdate,
    session: AsyncSession = Depends(get_session),
) -> AppSetting:
    setting = await session.get(AppSetting, key)
    if setting is None:
        setting = AppSetting(key=key, value=payload.value)
        session.add(setting)
    else:
        setting.value = payload.value
    await session.commit()
    await session.refresh(setting)
    return setting
