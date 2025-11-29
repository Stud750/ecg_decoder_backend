from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import dotenv_values

env_variable = dotenv_values(".env")


DATABASE_URL = env_variable["DATABASE_URL"]

engine = create_async_engine(DATABASE_URL, echo=False)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session():
    async with async_session_maker() as session:
        yield session

