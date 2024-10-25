from fastapi import HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from src.uitils.scheme import SUser
from src.services.api.v1.vacancy_service.models import VacancyModel
from src.services.api.v1.vacancy_service.scheme import WorkCategory, VacancyResponse
from sqlalchemy import select
import asyncio
import logging
from src.requests.request import GET_USER_REQUEST

log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


class VacancyService:

    def __init__(
        self,
        session: AsyncSession,
        current_user: SUser,
        response: VacancyResponse,
        user_response: SUser,
    ):
        self.session = session
        self.current_user = current_user
        self.vacansy_response = response
        self.user_response = user_response

    async def create_vacancy(
        self,
        work_category: WorkCategory,
        vacancy_title: str = Form(...),
        experience: int = Form(...),
        key_skils: str = Form(...),
        is_exist: bool = Form(...),
        location: str = Form(...),
        description: str = Form(...),
        conditions: str = Form(...),
        price: int = Form(...),
    ):

        if self.current_user.role != "Работодотель":
            raise HTTPException(
                detail="Вы не сможете создать вакансию !", status_code=403
            )

        vacancy = VacancyModel(
            work_category=work_category,
            vacancy_title=vacancy_title,
            experience=experience,
            key_skils=key_skils,
            is_exist=is_exist,
            location=location,
            description=description,
            conditions=conditions,
            price=price,
            user_id=self.current_user.id,
        )

        self.session.add(vacancy)
        await self.session.commit()

    async def get_vacancy(self, id: str) -> VacancyResponse | None:

        vacancy_query = await self.session.execute(
            select(VacancyModel).filter_by(id=id, is_exist=True)
        )

        vacancy = vacancy_query.scalars().first()
        if not vacancy:
            raise HTTPException(detail="Vacancy not found", status_code=404)

        tasks = [self.fetch_user_data(vacancy.user_id)]

        response = await asyncio.gather(*tasks)

        user_data = response[0]

        response = VacancyResponse(
            id=vacancy.id,
            vacancy_title=vacancy.vacancy_title,
            date_pub=vacancy.date_of_pub,
            description=vacancy.description,
            conditions=vacancy.conditions,
            experience=vacancy.experience,
            is_exist=vacancy.is_exist,
            price=vacancy.price,
            key_skils=vacancy.key_skils,
            location=vacancy.location,
            work_category=vacancy.work_category,
            user=(
                SUser(
                    id=user_data.get("id"),
                    username=user_data.get("username"),
                    picture_url=user_data.get("picture_url"),
                    company_name=user_data.get("company_name"),
                    role=user_data.get("role"),
                    surname=user_data.get("surname"),
                    name=user_data.get("name"),
                    email=user_data.get("email"),
                    age=user_data.get("age"),
                )
                if user_data
                else None
            ),
        )

        return response

    async def vacancy_for_user(self):

        user_cv_data = await self.fetch_user_cv(self.current_user.id)

        work_category = user_cv_data.get("post")

        if work_category is None:
            raise HTTPException(
                status_code=404, detail="User CV or work category not found"
            )

        vacancy_query = await self.session.execute(
            select(VacancyModel)
            .filter_by(work_category=work_category, is_exist=True)
            .order_by(VacancyModel.date_of_pub.desc())
        )

        vacancys = vacancy_query.scalars().all()
        if not vacancys:
            return []

        get_user = [self.fetch_user_data(vacancy.user_id) for vacancy in vacancys]

        request_to_get_user = await asyncio.gather(*get_user)

        user_data = request_to_get_user[0]

        response = [
            VacancyResponse(
                id=vacancy.id,
                vacancy_title=vacancy.vacancy_title,
                experience=vacancy.experience,
                is_exist=vacancy.is_exist,
                price=vacancy.price,
                work_category=vacancy.work_category,
                location=vacancy.location,
                description=vacancy.description,
                key_skils=vacancy.key_skils,
                date_pub=vacancy.date_of_pub,
                user=(
                    SUser(
                        id=user_data.get("id"),
                        username=user_data.get("username"),
                        role=user_data.get("role"),
                        name=user_data.get("name"),
                        surname=user_data.get("surname"),
                        email=user_data.get("email"),
                        age=user_data.get("age"),
                        company_name=user_data.get("company_name"),
                        picture_url=user_data.get("picture_url"),
                    )
                    if user_data
                    else None
                ),
                conditions=vacancy.conditions,
            )
            for vacancy in vacancys
        ]

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

    async def fetch_user_cv(self, user_id: int):
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.current_user.token}"}

                response = await client.get(
                    f"http://localhost:8000/cv-service/api/v1/get-user-cv/{user_id}/",
                    headers=headers,
                )

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except httpx.HTTPError as e:
            print(f"Error occurred while fetching user CV: {e}")
            return None

    async def get_vacancy_by_category(self, category: WorkCategory, price: int = 0):

        vacancy_query = await self.session.execute(
            select(VacancyModel)
            .filter(VacancyModel.work_category == category)
            .filter(VacancyModel.price <= price)
            .filter(VacancyModel.is_exist != False)
            .order_by(VacancyModel.date_of_pub.desc())
        )

        vacancys = vacancy_query.scalars().all()
        if not vacancys:
            return []

        get_user_from_vacancy = [
            self.fetch_user_data(vacancy.user_id) for vacancy in vacancys
        ]

        request = await asyncio.gather(*get_user_from_vacancy)

        user_data = request[0]

        vacancy_response = [
            VacancyResponse(
                id=vacancy.id,
                vacancy_title=vacancy.vacancy_title,
                price=vacancy.price,
                experience=vacancy.experience,
                key_skils=vacancy.key_skils,
                conditions=vacancy.conditions,
                date_pub=vacancy.date_of_pub,
                location=vacancy.location,
                description=vacancy.description,
                user=(
                    SUser(
                        id=user_data.get("id"),
                        username=user_data.get("username"),
                        company_name=user_data.get("company_name"),
                        email=user_data.get("email"),
                        role=user_data.get("role"),
                        age=user_data.get("age"),
                        surname=user_data.get("surname"),
                        name=user_data.get("name"),
                        picture_url=user_data.get("picture_url"),
                    )
                    if user_data
                    else None
                ),
                is_exist=vacancy.is_exist,
                work_category=vacancy.work_category,
            )
            for vacancy in vacancys
        ]

        return vacancy_response

    async def update_vacancy_by_id(
        self,
        vacancy_id: str,
        vacancy_title: str,
        vacancy_category: WorkCategory,
        price: int,
        key_skils: str,
        experience: str,
        location: str,
        description: str,
        is_exist: bool,
        conditions: str,
    ):

        vacancy_query = await self.session.execute(
            select(VacancyModel).filter_by(user_id=self.current_user.id, id=vacancy_id)
        )

        vacancy = vacancy_query.scalars().first()
        if not vacancy:
            raise HTTPException(detail="Not Found", status_code=404)

        vacancy.conditions = conditions
        vacancy.description = description
        vacancy.experience = experience
        vacancy.key_skils = key_skils
        vacancy.vacancy_title = vacancy_title
        vacancy.price = price
        vacancy.work_category = vacancy_category
        vacancy.location = location
        vacancy.is_exist = is_exist

        await self.session.commit()

        return {"detail": "Updated Succsesfully"}

    async def get_all_user_vacancy(self, user_id: int) -> list[VacancyResponse] | None:

        vacancy_query = await self.session.execute(
            select(VacancyModel)
            .filter(VacancyModel.user_id == user_id)
            .order_by(VacancyModel.date_of_pub.desc())
        )

        vacancys = vacancy_query.scalars().all()
        if not vacancys:
            log.info(f"User with id {user_id} dont have vacancy")
            return []

        response = [
            VacancyResponse(
                id=vacancy.id,
                vacancy_title=vacancy.vacancy_title,
                description=vacancy.description,
                price=vacancy.price,
                location=vacancy.location,
                key_skils=vacancy.key_skils,
                experience=vacancy.experience,
                date_pub=vacancy.date_of_pub,
                conditions=vacancy.conditions,
                work_category=vacancy.work_category,
                is_exist=vacancy.is_exist,
                user_id=vacancy.user_id,
            )
            for vacancy in vacancys
        ]

        return response

    async def delete_vacancy(self, vacancy_id: str):

        vacancy_query = await self.session.execute(
            select(VacancyModel).filter_by(user_id=self.current_user.id, id=vacancy_id)
        )

        vacancy = vacancy_query.scalars().first()
        if not vacancy:
            log.info("Vacancy Not Found")
            raise HTTPException(detail="Not Found", status_code=404)

        await self.session.delete(vacancy)
        await self.session.commit()
        log.info("Deleted Succsesfully")

        return {"detail": "Deleted Sucsesfully"}
    