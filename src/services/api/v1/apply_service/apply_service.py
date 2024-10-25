from fastapi import HTTPException, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.api.v1.apply_service.models import ApplyModel
import httpx
from src.uitils.scheme import SUser
from sqlalchemy import select
import asyncio
from src.services.api.v1.apply_service.scheme import (
    ApplyResponse,
    CvResponse,
    VacancyResponse,
)
from fastapi_mail import FastMail, MessageSchema
from src.config.email import conf
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



class ApllyService:

    def __init__(self, session: AsyncSession, current_user: SUser):
        self.session = session
        self.current_user = current_user

    async def create_apply(self, vacancy_id: str, latter: str = Form(None)):

        exist_apply_query = await self.session.execute(
            select(ApplyModel)
            .filter_by(user_id=self.current_user.id, vacancy_id=vacancy_id)
            .order_by(ApplyModel.created_at.desc())
        )

        exist_apply = exist_apply_query.scalars().first()

        if exist_apply:
            raise HTTPException(
                detail="You already applied for this vacancy", status_code=403
            )
        user_cv_data = await self.fetch_cv_data(self.current_user.id)

        cv_data = user_cv_data

        if not cv_data:
            raise HTTPException(
                detail="You dont have cv Please Create CV!", status_code=403
            )

        request_vacancy_data = [self.fetch_vacance_data(vacancy_id=vacancy_id)]

        vacancy_data_req = await asyncio.gather(*request_vacancy_data)

        vacancy_data = vacancy_data_req[0]
        if not vacancy_data:
            raise HTTPException(detail="Vacancy not found", status_code=404)

        message = MessageSchema(
            subject="Vacancy Request",
            recipients=[self.current_user.email],
            body=f"You Apply this vacancy: vacancy title and vacancy_id {vacancy_data.get("vacancy_title")}",
            subtype="plain",
        )

        fm = FastMail(conf)
        await fm.send_message(message)


        if vacancy_data.get("user"):
        
            author_message = MessageSchema(
                subject="Vacancy Author Request ",
                recipients=[vacancy_data.get("user").get("email")],
                body=f"User with username {self.current_user.username} applyted to your vacancy {vacancy_data.get("vacancy_title")}",
                subtype="plain",
            )

            fm = FastMail(conf)
            await fm.send_message(author_message)

        apply = ApplyModel(
            user_id=self.current_user.id,
            vacancy_id=vacancy_data.get("id"),
            cv_id=cv_data.get("id") if cv_data else None,
            latter=latter if latter else None,
            status="Не просмотрён",
        )

        self.session.add(apply)
        await self.session.commit()

    async def fetch_cv_data(self, user_id: int):
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.current_user.token}"}

                response_for_get_cv = await client.get(
                    f"http://localhost:8000/cv-service/api/v1/get-user-cv/{user_id}/",
                    headers=headers,
                )

            if response_for_get_cv.status_code == 200:
                return response_for_get_cv.json()

            else:
                return None

        except Exception as e:
            return None

    async def fetch_vacance_data(self, vacancy_id: int):
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.current_user.token}"}

                response_for_get_cv = await client.get(
                    f"http://localhost:8000/vacancy-service/api/v1/get-vacancy/{vacancy_id}/",
                    headers=headers,
                )

            if response_for_get_cv.status_code == 200:
                return response_for_get_cv.json()

            else:
                return None

        except Exception as e:
            return None

    async def fetch_user_data(self, user_id: int):
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.current_user.token}"}

                response_for_get_cv = await client.get(
                    f"http://192.168.100.59:8000/user-service/api/v1/get-user/{user_id}/",
                    headers=headers,
                )

            if response_for_get_cv.status_code == 200:
                return response_for_get_cv.json()

            else:
                return None

        except Exception as e:
            return None

    async def get_applys_from_vacance(self, vacance_id: str):

        applys_query = await self.session.execute(
            select(ApplyModel)
            .filter_by(vacancy_id=vacance_id)
            .order_by(ApplyModel.created_at.desc())
        )

        applys = applys_query.scalars().all()

        if not applys:
            return []

        request_to_user_data = [
            self.fetch_user_data(apply_obj.user_id) for apply_obj in applys
        ]
        user_data_response = await asyncio.gather(*request_to_user_data)

        user_cv_data_req = [
            self.fetch_cv_data(
                apply_obj.user_id
            ) 
            for apply_obj in applys
        ]
        cv_data_response = await asyncio.gather(*user_cv_data_req)


        response = [
            ApplyResponse(
                id=apply_obj.id,
                user=SUser(
                    id=user_data.get("id"),
                    username=user_data.get("username"),
                    email=user_data.get("email"),
                    age=user_data.get("age"),
                    picture_url=user_data.get("picture_url"),
                    name=user_data.get("name"),
                    surname=user_data.get("surname"),
                    company_name=user_data.get("company_name"),
                    role=user_data.get("role"),
                ),
                cv_response=CvResponse(
                    id=cv_data.get("id") if isinstance(cv_data, dict) else None,
                    specialization=(
                        cv_data.get("specialization")
                        if isinstance(cv_data, dict)
                        else None
                    ),
                    post=cv_data.get("post") if isinstance(cv_data, dict) else None,
                    skils=cv_data.get("skils") if isinstance(cv_data, dict) else None,
                    about_of_me=(
                        cv_data.get("about_of_me")
                        if isinstance(cv_data, dict)
                        else None
                    ),
                    schedule=(
                        cv_data.get("schedule") if isinstance(cv_data, dict) else None
                    ),
                    experience=(
                        cv_data.get("experience") if isinstance(cv_data, dict) else None
                    ),
                    experience_about=(
                        cv_data.get("experience_about")
                        if isinstance(cv_data, dict)
                        else None
                    ),
                    create_at=(
                        cv_data.get("create_at") if isinstance(cv_data, dict) else None
                    ),
                    amusement=(
                        cv_data.get("amusement") if isinstance(cv_data, dict) else None
                    ),
                ),
                status=apply_obj.status,
                created_at=apply_obj.created_at,
                user_id=apply_obj.user_id,
            )
            for apply_obj, user_data, cv_data in zip(
                applys, user_data_response, cv_data_response
            )
        ]

        return response
    

    async def get_user_applys(self):

        applys_query = await self.session.execute(
            select(ApplyModel)
            .filter(ApplyModel.user_id == self.current_user.id)
            .order_by(ApplyModel.created_at.desc())
        )

        apply = applys_query.scalars().all()

        get_vacancy = [
            self.fetch_vacance_data(apply_obj.vacancy_id) for apply_obj in apply
        ]

        vacancy_data_req = await asyncio.gather(*get_vacancy)

        vacancy_data = vacancy_data_req[0]

        response = [
            ApplyResponse(
                id=apply_obj.id,
                vacancy=VacancyResponse(
                    id=vacancy_data.get("id"),
                    vacancy_title=vacancy_data.get("vacancy_title"),
                    work_category=vacancy_data.get("work_category"),
                    is_exist=vacancy_data.get("is_exist"),
                    price=vacancy_data.get("price"),
                    key_skils=vacancy_data.get("key_skils"),
                    experience=vacancy_data.get("experience"),
                    date_pub=vacancy_data.get("date_pub"),
                    location=vacancy_data.get("location"),
                    description=vacancy_data.get("description"),
                    conditions=vacancy_data.get("conditions"),
                    user=(
                        SUser(
                            id=vacancy_data.get("user").get("id"),
                            username=vacancy_data.get("user").get("username"),
                            email=vacancy_data.get("user").get("email"),
                            age=vacancy_data.get("user").get("age"),
                            name=vacancy_data.get("user").get("name"),
                            surname=vacancy_data.get("user").get("surname"),
                            company_name=vacancy_data.get("user").get("company_name"),
                            role=vacancy_data.get("user").get("role"),
                            picture_url=vacancy_data.get("user").get("picture_url"),
                        )
                        if vacancy_data.get("user")
                        else None
                    ),
                ),
                created_at=apply_obj.created_at,
                status=apply_obj.status,
                user_id=apply_obj.user_id,
            )
            for apply_obj in apply
        ]

        return response

    async def delete_apply(self, apply_id: int):

        apply_query = await self.session.execute(
            select(ApplyModel).filter_by(user_id=self.current_user.id, id=apply_id)
        )

        apply = apply_query.scalars().first()
        if not apply:
            raise HTTPException(detail="Not Found", status_code=404)

        await self.session.delete(apply)
        await self.session.commit()

        return {"detail": "Deleted Succsesfully"}

    
    async def update_apply_status(self, apply_id: int, status: str, latter: str = None):

        apply_query = await self.session.execute(

            select(ApplyModel)
            .filter(ApplyModel.id == apply_id)

        )

        apply = apply_query.scalars().first()


        get_user_data = await self.fetch_user_data(apply.user_id) 

        # user_data_response = await asyncio.gather(*get_user_data)

        user_data = get_user_data
        
        if not apply:
            log.info("Not Found")
            raise HTTPException(
                detail = "Not Found",
                status_code=404 
            )

        
        message = MessageSchema(
            subject="Apply Request",
            recipients=[user_data.get("email")],
            body=f"{self.current_user.username} Компания {self.current_user.company_name},  {status}, {latter}",
            subtype="plain",
            )

        fm = FastMail(conf)
        await fm.send_message(message)

        
        apply.status = status

        await self.session.commit()

        log.info("Updated Succsesfully")


        return {"detail": f"STATUS {status}"}
    
