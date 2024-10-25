from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+asyncpg://username:password@port/VacancyDB"

VacancyServiceDB = declarative_base()

vc_engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(class_=AsyncSession, bind=vc_engine)


async def get_vacancy_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
