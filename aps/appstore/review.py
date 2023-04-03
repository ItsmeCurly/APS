from typing import Any
from aps.appstore import constants
from pydantic import BaseModel, conint
import requests

from aps.db.core import SessionLocal

from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from aps.db.models.base import Base
from aps.utils import create_db_obj, flatten


class AppStoreReview(Base):
    __tablename__ = "appstore_review"

    username = Column(String)
    review_uri = Column(String)
    updated_at = Column(String)
    score = Column(Integer)
    review_version = Column(String)
    review_id = Column(String, primary_key=True, unique=True)
    title = Column(String)
    content = Column(String)
    vote_sum = Column(Integer)
    vote_count = Column(Integer)

    app_id = Column(String, ForeignKey("appstore_app.app_id"))
    app = relationship("AppStoreApp", backref="application", foreign_keys=[app_id])


class AppStoreReviewModel(BaseModel):
    username: str | None = Field(None, alias="author_uri_label")
    review_uri: str | None = Field(None, alias="author_uri_label")
    updated_at: str | None = Field(None, alias="updated_label")
    score: int | None = Field(None, alias="im:rating_label")
    review_version: str | None = Field(None, alias="im:version_label")
    review_id: str | None = Field(None, alias="id_label")
    title: str | None = Field(None, alias="title_label")
    content: str | None = Field(None, alias="content_label")
    vote_sum: int | None = Field(None, alias="im:voteSum_label")
    vote_count: int | None = Field(None, alias="im:voteCount_label")


class _ReqOptions(BaseModel):
    app_id: int
    country: constants.Country
    sort: constants.Sort

    @property
    def market(self):
        return constants.Markets[self.country.upper()]


# async def reviews(
#     category: int,
#     limit: int,
#     country: str,
#     collection: str = constants.Collection.TOP_FREE_IOS,
# ) -> Any:
#     opts = _ReqOptions(collection=collection, category=category, limit=limit, country=country,)

#     sort = "/sortby=${opts.sort}" or ""

#     resp = requests.get(f"https://itunes.apple.com/{opts.country}/rss/customerreviews/page={page}/id=${opts.app_id}/{sort}/json")

#     return resp.json()['feed']['entry']


async def reviews_all(
    app_id: int,
    country: str,
    sort: str = constants.Sort.HELPFUL,
) -> Any:

    opts = _ReqOptions(
        app_id=app_id,
        country=country,
        sort=sort,
    )

    sort = f"/sortby={opts.sort}" or ""

    reviews = []
    for page in range(1, 11):
        resp = requests.get(
            f"https://itunes.apple.com/{opts.country}/rss/customerreviews/page={page}/id={opts.app_id}/{sort}/json"
        )
        if 'entry' in resp.json()['feed']:
            js = resp.json()["feed"]["entry"]
        else:
            return reviews
        
        for review in js:
            flat_review = flatten(review)
            
            review = AppStoreReviewModel(**flat_review)

            reviews.append(review)
    return reviews
