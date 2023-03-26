from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


async def create_db_obj(db_session: AsyncSession, model_class, obj: BaseModel):
    """
    Builds a database object from a data model

    Args:
        db_session (AsyncSession): The SQLAlchemy database session
        model_class (SQLAlchemy model class): _description_
        obj (BaseModel): The data model object
    """

    data = obj.dict()

    db_obj = model_class(**data)

    try:
        db_session.add(db_obj)
        await db_session.commit()
    except Exception as e:
        logger.error(e)
        await db_session.rollback()
