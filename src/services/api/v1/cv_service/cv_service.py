from fastapi import HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.services.api.v1.cv_service.models import CvModel
from src.uitils.scheme import SUser
from src.services.api.v1.vacancy_service.scheme import WorkCategory
import httpx
import logging
import asyncio
from src.services.api.v1.cv_service.scheme import CvResponse
from src.requests.request import GET_USER_REQUEST

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CvService:

    def __init__(self, session: AsyncSession, current_user: SUser):
        self.session = session
        self.current_user = current_user

    async def create_cv(
        self,
        specializitaion: str,
        post: WorkCategory,
        amusement: str,
        schedule: str,
        phone_number: int,
        exprience: int,
        exprience_about: str,
        skils: str,
        about_of_me: str,
    ):

        exist_cv_query = await self.session.execute(
            select(CvModel).filter(CvModel.user_id == self.current_user.id)
        )

        exist_cv = exist_cv_query.scalars().first()
        log.info("User have CV")
        if exist_cv:
            raise HTTPException(detail="You All ready have CV", status_code=403)

        if self.current_user.role != "Работник":
            log.warn("Role Error")
            raise HTTPException(
                detail="You can not create Cv because you are Employer", status_code=403
            )

        new_cv = CvModel(
            specialization=specializitaion,
            post=post,
            amusement=amusement,
            schedule=schedule,
            phone_number=phone_number,
            experience=exprience,
            experience_about=exprience_about,
            skils=skils,
            about_of_me=about_of_me,
            user_id=self.current_user.id,
        )

        self.session.add(new_cv)
        await self.session.commit()

        log.info("Created Succsesfully")

    async def get_user_cv(self, user_id: int):

        cv_query = await self.session.execute(
            select(CvModel).filter(CvModel.user_id == user_id)
        )

        cv = cv_query.scalars().first()
        if not cv:
            return []

        get_user_data = [self.fetch_user_data(cv.user_id)]

        request = await asyncio.gather(*get_user_data)

        user_data = request[0]

        response = CvResponse(
                id=cv.id,
                user=(
                    SUser(
                        id=user_data.get("id"),
                        username=user_data.get("username"),
                        email=user_data.get("email"),
                        age=user_data.get("age"),
                        picture_url=user_data.get("picture_url"),
                        name=user_data.get("name"),
                        surname=user_data.get("surname"),
                        role=user_data.get("role"),
                    )
                    if user_data
                    else None
                ),
                schedule=cv.schedule,
                specialization=cv.specialization,
                skils=cv.skils,
                experience=cv.experience,
                experience_about=cv.experience_about,
                create_at=cv.created_at,
                about_of_me=cv.about_of_me,
                amusement=cv.amusement,
                post=cv.post,
                )

        return response

    async def fetch_user_data(self, user_id: int):
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.current_user.token}"}
                response = await client.get(
                    f"{GET_USER_REQUEST}/{user_id}/",
                    headers=headers,
                )

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except Exception as e:
            return None

    

    async def update_cv_components(
        self,
        specializitaion: str,
        post: WorkCategory,
        amusement: str,
        schedule: str,
        phone_number: int,
        exprience: int,
        exprience_about: str,
        skils: str,
        about_of_me: str,

    ):
        
        user_query = await self.session.execute(

            select(CvModel)
            .filter(CvModel.user_id == self.current_user.id)

        )

        user = user_query.scalars().first()
        if not user:
            
            log.info("Cv Not Found")


            raise HTTPException(
                detail="Not Found",
                status_code=404
            )
        
        user.specialization = specializitaion
        user.post = post
        user.about_of_me = about_of_me
        user.schedule = schedule
        user.phone_number = phone_number
        user.amusement = amusement
        user.experience = exprience
        user.experience_about = exprience_about
        user.skils = skils

        await self.session.commit()

        log.info("Components Update Succsesfully")

        return {"Updated Succsesfully"}
    