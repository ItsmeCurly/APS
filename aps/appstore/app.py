import requests
from bs4 import BeautifulSoup
from loguru import logger
from pydantic import BaseModel, Field, conint
from sqlalchemy import Column, String

from aps.appstore import constants
from aps.db.models.base import Base
from aps.utils import flatten


class AppStoreApp(Base):
    __tablename__ = "appstore_app"

    app_id = Column(String, primary_key=True, unique=True)
    app_name = Column(String)
    summary = Column(String)
    price = Column(String)
    rights = Column(String)
    title = Column(String)
    app_uri = Column(String)
    app_bundle = Column(String)
    artist = Column(String)
    artist_uri = Column(String)
    app_category_id = Column(String)
    app_category_name = Column(String)
    app_category_uri = Column(String)
    app_release_date = Column(String)


class AppStoreAppBase(BaseModel):
    app_id: str
    app_name: str

    async def reviews_all(self, sort: constants.Sort = constants.Sort.HELPFUL) -> list:
        from aps.appstore.review import reviews_all

        logger.info(f"Retrieving reviews from {self.app_id} {sort=}")

        return await reviews_all(app_id=self.app_id, country="us")

    async def reviews(self):
        from .scraper import AppStore

        app = AppStore(country="us", app_name=self.app_name, app_id=self.app_id)

        return app.review()

    async def similar_cluster(self):
        resp = requests.get(f"https://play.google.com/store/apps/details?id={self.id}")

        soup = BeautifulSoup(resp.text, "lxml")

        for a in soup.find_all("a"):
            if "collection" in a["href"]:
                return a["href"]


class AppStoreAppModel(AppStoreAppBase):
    app_id: str | None = Field(None, alias="id_attributes_im:id")
    app_name: str | None = Field(None, alias="im:name_label")
    summary: str | None = Field(None, alias="summary_label")
    price: str | None = Field(None, alias="im:price_attributes_amount")
    rights: str | None = Field(None, alias="rights_label")
    title: str | None = Field(None, alias="title_label")
    app_uri: str | None = Field(None, alias="id_label")
    app_bundle: str | None = Field(None, alias="id_attributes_im:bundleId")
    artist: str | None = Field(None, alias="im:artist_label")
    artist_uri: str | None = Field(None, alias="im:artist_attributes_href")
    app_category_id: str | None = Field(None, alias="category_attributes_im:id")
    app_category_name: str | None = Field(None, alias="category_attributes_term")
    app_category_uri: str | None = Field(None, alias="category_attributes_scheme")
    app_release_date: str | None = Field(None, alias="im:releaseDate_label")


class ReqOptions(BaseModel):
    collection: constants.Collection
    category: constants.Category
    limit: conint(le=200)
    country: constants.Country

    @property
    def market(self):
        return constants.Markets[self.country.upper()]


async def apps_all(
    category: int,
    limit: int,
    country: str,
    collection: str = constants.Collection.TOP_FREE_IOS,
) -> list[AppStoreAppModel]:
    opts = ReqOptions(
        collection=collection,
        category=category,
        limit=limit,
        country=country,
    )

    logger.info(f"Retrieving apps with options {opts}")

    category = f"/genre={opts.category}" or ""

    resp = requests.get(
        f"http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/{opts.collection}/{category}/limit={opts.limit}/json?s={opts.market}"
    )

    content = resp.json()["feed"]["entry"]
    apps = []

    for app in content:
        flat_app = flatten(app)

        app = AppStoreAppModel(**flat_app)

        apps.append(app)
    logger.info(f"Found {len(apps)} apps")
    return apps
