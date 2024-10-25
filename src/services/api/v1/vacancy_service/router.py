from fastapi import Depends, APIRouter, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.api.v1.vacancy_service.vacancy_service import (
    VacancyService,
    SUser,
    WorkCategory,
    VacancyResponse,
)
from src.uitils.uitils import get_current_user
from src.config.database import get_vacancy_session


vacancy_router = APIRouter(tags=["Vacancy Service"], prefix="/vacancy-service/api/v1")


@vacancy_router.post("/create-vacancy/")
async def create_vacancy(
    work_category: WorkCategory,
    session: AsyncSession = Depends(get_vacancy_session),
    current_user: SUser = Depends(get_current_user),
    vacancy_title: str = Form(...),
    exeprience: int = Form(...),
    key_skils: str = Form(...),
    is_exist: bool = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    conditions: str = Form(...),
    price: int = Form(...),
):

    category = work_category.value

    vacancy_service = VacancyService(
        session=session,
        current_user=current_user,
        user_response=SUser,
        response=VacancyResponse,
    )
    return await vacancy_service.create_vacancy(
        work_category=category,
        vacancy_title=vacancy_title,
        experience=exeprience,
        key_skils=key_skils,
        is_exist=is_exist,
        location=location,
        description=description,
        price=price,
        conditions=conditions,
    )


@vacancy_router.get("/get-vacancy/{id}/", response_model=VacancyResponse)
async def get_vacancy(
    id: str,
    session: AsyncSession = Depends(get_vacancy_session),
    current_user: SUser = Depends(get_current_user),
):
    service = VacancyService(
        session=session,
        response=VacancyResponse,
        current_user=current_user,
        user_response=SUser,
    )
    return await service.get_vacancy(id=id)


@vacancy_router.get("/get-vacancy-for-user/", response_model=list[VacancyResponse])
async def get_vacancy_for_user(
    session: AsyncSession = Depends(get_vacancy_session),
    current_user: SUser = Depends(get_current_user),
):
    service = VacancyService(
        session=session,
        current_user=current_user,
        user_response=SUser,
        response=VacancyResponse,
    )
    return await service.vacancy_for_user()


@vacancy_router.get(
    "/get-vacancy-by-category/{category}/{price}/", response_model=list[VacancyResponse]
)
async def get_vacancy_by_category(
    category: WorkCategory,
    price: int = 0,
    session: AsyncSession = Depends(get_vacancy_session),
    current_user: SUser = Depends(get_current_user),
):
    service = VacancyService(
        session=session,
        current_user=current_user,
        response=VacancyResponse,
        user_response=SUser,
    )
    work_category = category.value
    return await service.get_vacancy_by_category(category=work_category, price=price)


@vacancy_router.get(
    "/get-user-vacancy/{user_id}/", response_model=list[VacancyResponse]
)
async def get_user_vacancy(
    user_id: int,
    session: AsyncSession = Depends(get_vacancy_session),
    current_user: SUser = Depends(get_current_user),
):
    service = VacancyService(
        session=session,
        response=VacancyResponse,
        current_user=current_user,
        user_response=SUser,
    )
    return await service.get_all_user_vacancy(user_id=user_id)


@vacancy_router.patch("/update-vacancy/{vacancy_id}/")
async def update_vacancy(
    vacancy_id: str,
    work_category: WorkCategory,
    session: AsyncSession = Depends(get_vacancy_session),
    current_user: SUser = Depends(get_current_user),
    vacancy_title: str = Form(...),
    exeprience: int = Form(...),
    key_skils: str = Form(...),
    is_exist: bool = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    conditions: str = Form(...),
    price: int = Form(...),
):

    category = work_category.value

    service = VacancyService(
        session=session,
        current_user=current_user,
        response=VacancyResponse,
        user_response=SUser,
    )
    return await service.update_vacancy_by_id(
        vacancy_category=category,
        vacancy_title=vacancy_title,
        vacancy_id=vacancy_id,
        key_skils=key_skils,
        description=description,
        conditions=conditions,
        experience=exeprience,
        price=price,
        location=location,
        is_exist=is_exist,
    )


@vacancy_router.delete("/delete-vacancy/{vacancy_id}/")
async def delete_user_vacancy(
    vacancy_id: str,
    session: AsyncSession = Depends(get_vacancy_session),
    current_user: SUser = Depends(get_current_user),
):

    service = VacancyService(
        session=session,
        current_user=current_user,
        response=VacancyResponse,
        user_response=SUser,
    )
    return await service.delete_vacancy(vacancy_id)
