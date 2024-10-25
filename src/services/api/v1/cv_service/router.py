from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.cv_database import get_cv_session
from src.services.api.v1.cv_service.cv_service import (
    CvService,
    SUser,
    WorkCategory,
    CvResponse,
)
from src.uitils.uitils import get_current_user
from src.services.api.v1.cv_service.scheme import CVUpdateRequest


cv_service_router = APIRouter(tags=["User CV Service"], prefix="/cv-service/api/v1")


@cv_service_router.post("/create-cv/")
async def create_cv(
    post: WorkCategory,
    session: AsyncSession = Depends(get_cv_session),
    current_user: SUser = Depends(get_current_user),
    specializitaion: str = Form(...),
    amusement: str = Form(...),
    schedule: str = Form(...),
    phone_number: int = Form(...),
    exprience: int = Form(...),
    exprience_about: str = Form(...),
    skils: str = Form(...),
    about_of_me: str = Form(...),
):

    service = CvService(session=session, current_user=current_user)
    work_cateogory = post.value
    return await service.create_cv(
        post=work_cateogory,
        schedule=schedule,
        specializitaion=specializitaion,
        amusement=amusement,
        phone_number=phone_number,
        exprience=exprience,
        exprience_about=exprience_about,
        skils=skils,
        about_of_me=about_of_me,
    )


@cv_service_router.get("/get-user-cv/{user_id}/", response_model=CvResponse)
async def get_user_cv_(
    user_id: int,
    session: AsyncSession = Depends(get_cv_session),
    current_user: SUser = Depends(get_current_user),
):
    service = CvService(session=session, current_user=current_user)
    return await service.get_user_cv(user_id=user_id)





@cv_service_router.patch("/update-user-components/{post}/")
async def update_user_cv(post: WorkCategory, request: CVUpdateRequest,  session: AsyncSession = Depends(get_cv_session), current_user: SUser = Depends(get_current_user)):
    service = CvService(session=session, current_user=current_user)
    post_ = post.value

    request_data = request.dict()

    return await service.update_cv_components(**request_data, post = post_)
