from sqlalchemy import Column, Integer
from aps.db.models.base import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
