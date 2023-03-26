from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from aps.db.models.base import Base


class Review(Base):
    __tablename__ = "review"

    review_id = Column(String, primary_key=True, unique=True)
    username = Column(String)
    user_image = Column(String)
    content = Column(String)
    score = Column(Integer)
    thumbs_up_count = Column(Integer)
    review_created_version = Column(String)
    posted_at = Column(DateTime)
    reply_content = Column(String)
    reply_at = Column(DateTime)

    app_id = Column(String, ForeignKey("application.app_id"))
    app = relationship("Application", backref="application", foreign_keys=[app_id])


class ReviewModel(BaseModel):
    review_id: str | None = Field(None, alias="reviewId")
    username: str | None = Field(None, alias="userName")
    user_image: str | None = Field(None, alias="userImage")
    content: str | None = Field(None, alias="content")
    score: int | None = Field(None, alias="score")
    thumbs_up_count: int | None = Field(None, alias="thumbsUpCount")
    review_created_version: str | None = Field(None, alias="reviewCreatedVersion")
    posted_at: datetime | None = Field(None, alias="at")
    reply_content: str | None = Field(None, alias="replyContent")
    reply_at: datetime | None = Field(None, alias="repliedAt")

    app_id: str
