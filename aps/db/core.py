from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from aps.conf import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, poolclass=NullPool
)

SessionLocal = orm.sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
