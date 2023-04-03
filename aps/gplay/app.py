import asyncio
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from aps.db.models.base import Base


class GPlayApp(Base):
    __tablename__ = "gplay_app"

    app_id = Column(String, primary_key=True, unique=True)
    title = Column(String)
    description = Column(String)
    summary = Column(String)
    installs = Column(String)
    min_installs = Column(Integer)
    real_installs = Column(Integer)
    score = Column(Float)
    num_ratings = Column(Integer)
    num_reviews = Column(Integer)
    price = Column(Float)
    free = Column(Boolean)
    currency = Column(String)
    sale = Column(String)
    developer = Column(String)
    developer_id = Column(String)
    developer_email = Column(String)
    developer_website = Column(String)
    privacy_policy = Column(String)
    genre = Column(String)
    genre_id = Column(String)
    icon = Column(String)
    header_image = Column(String)
    video = Column(String)
    video_image = Column(String)
    content_rating = Column(String)
    ad_supported = Column(Boolean)
    contains_ads = Column(Boolean)
    released = Column(DateTime)
    updated = Column(DateTime)
    version = Column(String)
    url = Column(String)


class GPlayAppBase(BaseModel):
    app_id: str | None = Field(None, alias="id")

    async def reviews_all(self, sleep_milliseconds: int = 0, **kwargs) -> list:
        from google_play_scraper.features.reviews import (MAX_COUNT_EACH_FETCH,
                                                          reviews)

        kwargs.pop("count", None)
        kwargs.pop("continuation_token", None)

        continuation_token = None

        while True:
            _result, continuation_token = reviews(
                self.app_id,
                count=MAX_COUNT_EACH_FETCH,
                continuation_token=continuation_token,
                **kwargs,
            )

            yield _result

            if continuation_token.token is None:
                break

            if sleep_milliseconds:
                await asyncio.sleep(sleep_milliseconds / 1000)

    async def reviews(self):
        from google_play_scraper import reviews_all

        return reviews_all(app_id=self.app_id, sleep_milliseconds=1000)

    async def similar_cluster(self):
        resp = requests.get(f"https://play.google.com/store/apps/details?id={self.id}")

        soup = BeautifulSoup(resp.text, "lxml")

        for a in soup.find_all("a"):
            if "collection" in a["href"]:
                return a["href"]


class GPlayAppModel(GPlayAppBase):
    app_id: str | None = Field(None, alias="appId")
    title: str | None = Field(None, alias="title")
    description: str | None = Field(None, alias="description")
    summary: str | None = Field(None, alias="summary")
    installs: str | None = Field(None, alias="installs")
    min_installs: int | None = Field(None, alias="minInstalls")
    real_installs: int | None = Field(None, alias="realInstalls")
    score: float | None = Field(None, alias="score")
    num_ratings: int | None = Field(None, alias="ratings")
    num_reviews: int | None = Field(None, alias="reviews")
    price: float | None = Field(None, alias="price")
    free: bool | None = Field(None, alias="free")
    currency: str | None = Field(None, alias="currency")
    sale: str | None = Field(None, alias="sale")
    developer: str | None = Field(None, alias="developer")
    developer_id: str | None = Field(None, alias="developerId")
    developer_email: str | None = Field(None, alias="developerEmail")
    developer_website: str | None = Field(None, alias="developerWebsite")
    privacy_policy: str | None = Field(None, alias="privacyPolicy")
    genre: str | None = Field(None, alias="genre")
    genre_id: str | None = Field(None, alias="genreId")
    icon: str | None = Field(None, alias="icon")
    header_image: str | None = Field(None, alias="headerImage")
    video: str | None = Field(None, alias="video")
    video_image: str | None = Field(None, alias="videoImage")
    content_rating: str | None = Field(None, alias="contentRating")
    ad_supported: bool | None = Field(None, alias="adSupported")
    contains_ads: bool | None = Field(None, alias="containsAds")
    released: datetime | None = Field(None, alias="released")
    updated: datetime | None = Field(None, alias="updated")
    version: str | None = Field(None, alias="version")
    url: str | None = Field(None, alias="url")


class ChartApplication(GPlayAppBase):
    id: str | None = Field(None, alias="id")
    icon_url: str | None = Field(None, alias="icon_url")
    screenshot_urls: list[str]
    name: str | None = Field(None, alias="name")
    rating: float | None = Field(None, alias="rating")
    category: str | None = Field(None, alias="category")
    price: str | None = Field(None, alias="price")
    buy_url: str | None = Field(None, alias="buy_url")
    store_path: str | None = Field(None, alias="store_path")
    trailer_url: str | None = Field(None, alias="trailer_url")
    description: str | None = Field(None, alias="description")
    developer: str | None = Field(None, alias="developer")
    downloads: str | None = Field(None, alias="downloads")
    cover_image_url: str | None = Field(None, alias="cover_image_url")
