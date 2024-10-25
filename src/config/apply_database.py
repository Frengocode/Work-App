from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql+asyncpg://username:password@port/ApplyDB"

ApplyBASE  = declarative_base()

apply_engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(class_=AsyncSession, bind=apply_engine)


async def get_apply_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
