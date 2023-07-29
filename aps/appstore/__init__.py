import re
from enum import StrEnum

import requests
from bs4 import BeautifulSoup
from loguru import logger
from sqlalchemy import select

from aps.appstore.app import AppStoreApp
from aps.appstore.review import AppStoreReview
from aps.db.core import SessionLocal
from aps.gplay.app import GPlayAppModel
from aps.utils import create_db_obj

pat = re.compile(r"https:\/\/apps\.apple\.com\/us\/app\/([^\/]*)\/id([\d]+)")


class Platform(StrEnum):
    IPAD = "ipad"
    IPHONE = "iphone"


appcat = {
    "business": {"name": "business-apps", "id": "6000"},
    "books": {"name": "books-apps", "id": "6018"},
    "developer_tools": {"name": "developer-tools-apps", "id": "6026"},
    "education": {"name": "education-apps", "id": "6017"},
    "entertainment": {"name": "entertainment-apps", "id": "6016"},
    "finance": {"name": "finance-apps", "id": "6015"},
    "food_drink": {"name": "food-drink-apps", "id": "6023"},
    "graphics_design": {"name": "graphics-design-apps", "id": "6027"},
    "health_fitness": {"name": "health-fitness-apps", "id": "6013"},
    "kids": {"name": "kids-apps", "id": "36", "params": "ageId=0&ageId=0"},
    "lifestyle": {"name": "lifestyle-apps", "id": "6012"},
    "magazines_newspapers": {"name": "magazines-newspapers-apps", "id": "6021"},
    "medical": {"name": "medical-apps", "id": "6020"},
    "music": {"name": "music-apps", "id": "6011"},
    "navigation": {"name": "navigation-apps", "id": "6010"},
    "news": {"name": "news-apps", "id": "6009"},
    "photo_video": {"name": "photo-video-apps", "id": "6008"},
    "productivity": {"name": "productivity-apps", "id": "6007"},
    "reference": {"name": "reference-apps", "id": "6006"},
    "shopping": {"name": "shopping-apps", "id": "6024"},
    "social_networking": {"name": "social-networking-apps", "id": "6005"},
    "sports": {"name": "sports-apps", "id": "6004"},
    "top_free": {"name": "top-free-apps", "id": "36"},
    "top_paid": {"name": "top-paid-apps", "id": "36"},
    "travel": {"name": "travel-apps", "id": "6003"},
    "utilities": {"name": "utilities-apps", "id": "6002"},
    "weather": {"name": "weather-apps", "id": "6001"},
}

gamecat = {
    "top_free": {"name": "top-free-games", "id": "6014"},
    "top_paid": {"name": "top-paid-games", "id": "6014"},
    "action": {"name": "action-games", "id": "7001"},
    "adventure": {"name": "adventure-games", "id": "7002"},
    "board": {"name": "board-games", "id": "7004"},
    "card": {"name": "card-games", "id": "7005"},
    "casino": {"name": "casino-games", "id": "7006"},
    "casual": {"name": "casual-games", "id": "7003"},
    "family": {"name": "family-games", "id": "7009"},
    "music": {"name": "music-games", "id": "7011"},
    "puzzle": {"name": "puzzle-games", "id": "7012"},
    "racing": {"name": "racing-games", "id": "7013"},
    "role_playing": {"name": "role-playing-games", "id": "7014"},
    "simulation": {"name": "simulation-games", "id": "7015"},
    "sports": {"name": "sports-games", "id": "7016"},
    "strategy": {"name": "strategy-games", "id": "7017"},
    "trivia": {"name": "trivia-games", "id": "7018"},
    "word": {"name": "word-games", "id": "7019"},
}


class Chart(StrEnum):
    TOP_FREE = "top-free"
    TOP_PAID = "top-paid"


class AppStore:
    def __init__(
        self,
        base_apps_url: str = "https://apps.apple.com",
        base_itunes_url: str = "https://itunes.apple.com",
    ) -> None:
        self._base_apps_url = base_apps_url
        self._base_itunes_url = base_itunes_url

    async def _request_top(
        self,
        country: str,
        platform: str,
        category_name: str,
        category_id: str,
        chart: str,
        category_params: str | None = None,
    ) -> requests.Response:
        """
        Makes a request to the appstore for the top apps

        Args:
            country (str): Country to request on
            platform (str): Platform to request apps from
            category_name (str): Category name to request apps from
            category_id (str): Category id, matching category name
            chart (str): Chart to request apps from
            category_params (str | None, optional): Category params. Defaults to None.

        Returns:
            requests.Response: Response from the appstore
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "DNT": "1",
            "Sec-GPC": "1",
        }

        params = {
            "chart": chart,
        }

        if category_params:
            for param in category_params.split("&"):
                for pk, pv in param.split("="):
                    params[pk] = pv

        req_url = f"https://apps.apple.com/{country}/charts/{platform}/{category_name}/{category_id}"
        response = requests.get(
            req_url,
            params=params,
            headers=headers,
        )

        return response

    async def build_application_data(
        self, app_name: str, app_id: str, load_reviews: bool = True
    ) -> GPlayAppModel:
        pass

    async def fetch_top_charts(
        self,
        country: str,
        platform: str,
        category_name: str,
        category_id: str,
        chart: str,
        category_params: str | None = None,
    ) -> list[GPlayAppModel]:
        """
        Fetches top charts by scraping the appstore, a different approach from aps.appstore.app.apps_all().

        Not fully implemented.

        Args:
            country (str): Country to search, from constants.Country
            platform (str): Platform to search on, from constants.Platform
            category_name (str): Category name to search on, from constants.Category
            category_id (str): Category id to search on, from constants.Category
            chart (str): Chart to search on, from constants.Chart
            category_params (str | None, optional): Category params to include with the request, 
                from constants.Category, if present. Defaults to None.

        Returns:
            list[GPlayAppModel]: A list of the GPlay applications

        """

        response = await self._request_top(
            country=country,
            platform=platform,
            category_name=category_name,
            category_id=category_id,
            chart=chart,
            category_params=category_params,
        )
        soup = BeautifulSoup(response.text)

        urls = []
        for a in soup.find_all("a"):
            if "/app/" in a["href"]:
                urls.append(a["href"])

        for url in urls:
            matches = re.match(pat, url)

            matches.group(1)
            matches.group(2)

    async def fetch_similar(self, app: GPlayAppModel) -> list[GPlayAppModel]:
        """Not currently implemented :)"""

    async def fetch_all(self, load_reviews: bool = True):
        """
        Fetches all apps from the appstore that can be found
        """
        from aps.appstore import constants
        from aps.appstore.app import apps_all

        session = SessionLocal()
        limit = 100
        for category in constants.Category:
            for collection in constants.Collection:
                for country in constants.Country:
                    print(
                        f"Retrieving {limit} apps from {category=} / {collection=} / {country=}"
                    )
                    apps = await apps_all(
                        category=category,
                        limit=limit,
                        country=country,
                        collection=collection,
                    )

                    for app in apps:
                        result = await session.execute(
                            select(AppStoreApp).where(AppStoreApp.app_id == app.app_id)
                        )
                        db_obj = result.scalars().first()

                        if db_obj:
                            logger.info(f"App {app.app_id} already processed, skipping")
                            continue

                        await create_db_obj(
                            db_session=session, model_class=AppStoreApp, obj=app
                        )

                        if load_reviews:
                            for sort in constants.Sort:
                                reviews = await app.reviews_all(sort=sort)

                                if len(reviews) == 0:
                                    logger.info("No reviews found, skipping")
                                    break

                                for review in reviews:
                                    result = await session.execute(
                                        select(AppStoreReview).where(
                                            AppStoreReview.review_id == review.review_id
                                        )
                                    )
                                    db_obj = result.scalars().first()

                                    if db_obj:
                                        logger.info(
                                            f"Review {review.review_id} already processed, skipping"
                                        )
                                        continue
                                    await create_db_obj(
                                        db_session=session,
                                        model_class=AppStoreReview,
                                        obj=review,
                                    )

    async def fetch_all_recursive(self):
        """Not currently implemented :)"""
        await self.fetch_all()
