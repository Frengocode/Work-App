from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.uitils.uitils import get_current_user
from src.services.api.v1.apply_service.apply_service import (
    ApllyService,
    SUser,
    ApplyResponse,
)
from src.config.apply_database import get_apply_session


apply_service = APIRouter(tags=["Apply Service"], prefix="/apply-service/api/v1")


@apply_service.post("/create-apply/{vacancy_id}/")
async def create_apply_for_vacance(
    vacancy_id: str,
    latter: str = Form(None),
    session: AsyncSession = Depends(get_apply_session),
    current_user: SUser = Depends(get_current_user),
):
    service = ApllyService(session=session, current_user=current_user)
    return await service.create_apply(vacancy_id=vacancy_id, latter=latter)


@apply_service.get("/get-apllys/{vacance_id}/", response_model=list[ApplyResponse])
async def get_applys(
    vacance_id: str,
    session: AsyncSession = Depends(get_apply_session),
    current_user: SUser = Depends(get_current_user),
):
    service = ApllyService(session=session, current_user=current_user)
    return await service.get_applys_from_vacance(vacance_id=vacance_id)


@apply_service.get("/get-user-applys/", response_model=list[ApplyResponse])
async def get_user_apply(
    session: AsyncSession = Depends(get_apply_session),
    current_user: SUser = Depends(get_current_user),
):
    service = ApllyService(session=session, current_user=current_user)
    return await service.get_user_applys()


@apply_service.patch("/update-status/{apply_id}/{status}/{latter}/")
async def update_status(apply_id: int, status: str, latter: str = None, session: AsyncSession = Depends(get_apply_session), current_user: SUser = Depends(get_current_user)):
    service = ApllyService(session=session, current_user=current_user)
    return await service.update_apply_status(apply_id=apply_id, status=status, latter = latter)

@apply_service.delete("/delete-user-apply/{apply_id}")
async def delete_user_apply(
    apply_id: int,
    session: AsyncSession = Depends(get_apply_session),
    current_user: SUser = Depends(get_current_user),
):
    service = ApllyService(session=session, current_user=current_user)
    return await service.delete_apply(apply_id=apply_id)


