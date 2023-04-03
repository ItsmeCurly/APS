from typing import MutableMapping

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

        return db_obj
    except Exception as e:
        logger.error(e)
        await db_session.rollback()


def flatten(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
