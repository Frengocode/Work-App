from fastapi import FastAPI
from src.services.api.v1.vacancy_service.router import vacancy_router
from fastapi.middleware.cors import CORSMiddleware
from src.services.api.v1.cv_service.router import cv_service_router
from src.config.cv_database import cv_engine, CVServiceDB
from src.config.database import vc_engine, VacancyServiceDB
from src.services.api.v1.apply_service.router import apply_service
from src.config.apply_database import apply_engine, ApplyBASE


app = FastAPI(title="Vacancy Service & Apply Service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_tables():
    async with cv_engine.begin() as conn:
        await conn.run_sync(CVServiceDB.metadata.create_all)

    async with vc_engine.begin() as conn:
        await conn.run_sync(VacancyServiceDB.metadata.create_all)

    
    async with apply_engine.begin() as conn:
        await conn.run_sync(ApplyBASE.metadata.create_all)



@app.on_event("startup")
async def on_startup():
    await create_tables()


app.include_router(vacancy_router)
app.include_router(cv_service_router)
app.include_router(apply_service)

