import asyncio
import json
from datetime import datetime
from enum import IntEnum, StrEnum
from pprint import pprint
from typing import Any

import requests
from bs4 import BeautifulSoup
from loguru import logger
from sqlalchemy import select

from aps.db.core import SessionLocal
from aps.gplay.app import ChartApplication, GPlayApp, GPlayAppModel
from aps.gplay.review import GPlayReview, GPlayReviewModel
from aps.utils import create_db_obj

BASE_URL = "https://play.google.com"
APPS_BASE_URL = f"{BASE_URL}/store/apps"


class Cluster(StrEnum):
    NEW = "new"
    TOP = "top"


class Language(StrEnum):
    EN = "en"  # English


class Country(StrEnum):
    US = "us"  # United States
    UK = "gb"  # United Kingdom / Great Britin
    AU = "au"  # Australia
    CA = "ca"  # Canada
    BZ = "bz"  # Belize
    IE = "ie"  # Ireland
    JM = "jm"  # Jamaica
    NZ = "nz"  # New Zealand
    TT = "tt"  # Trinidad and Tobago
    ZA = "za"  # South Africa
    PH = "ph"  # Republic of the Philippines
    ZW = "zw"  # Zimbabwe
    CH = "ch"  # Chamorro


# LANGUAGE_CODES = f"{lang}-{country}


class Category(StrEnum):
    APPLICATION = "APPLICATION"
    ANDROID_WEAR = "ANDROID_WEAR"
    ART_AND_DESIGN = "ART_AND_DESIGN"
    AUTO_AND_VEHICLES = "AUTO_AND_VEHICLES"
    BEAUTY = "BEAUTY"
    BOOKS_AND_REFERENCE = "BOOKS_AND_REFERENCE"
    BUSINESS = "BUSINESS"
    COMICS = "COMICS"
    COMMUNICATION = "COMMUNICATION"
    DATING = "DATING"
    EDUCATION = "EDUCATION"
    ENTERTAINMENT = "ENTERTAINMENT"
    EVENTS = "EVENTS"
    FINANCE = "FINANCE"
    FOOD_AND_DRINK = "FOOD_AND_DRINK"
    HEALTH_AND_FITNESS = "HEALTH_AND_FITNESS"
    HOUSE_AND_HOME = "HOUSE_AND_HOME"
    LIBRARIES_AND_DEMO = "LIBRARIES_AND_DEMO"
    LIFESTYLE = "LIFESTYLE"
    MAPS_AND_NAVIGATION = "MAPS_AND_NAVIGATION"
    MEDICAL = "MEDICAL"
    MUSIC_AND_AUDIO = "MUSIC_AND_AUDIO"
    NEWS_AND_MAGAZINES = "NEWS_AND_MAGAZINES"
    PARENTING = "PARENTING"
    PERSONALIZATION = "PERSONALIZATION"
    PHOTOGRAPHY = "PHOTOGRAPHY"
    PRODUCTIVITY = "PRODUCTIVITY"
    SHOPPING = "SHOPPING"
    SOCIAL = "SOCIAL"
    SPORTS = "SPORTS"
    TOOLS = "TOOLS"
    TRAVEL_AND_LOCAL = "TRAVEL_AND_LOCAL"
    VIDEO_PLAYERS = "VIDEO_PLAYERS"
    WATCH_FACE = "WATCH_FACE"
    WEATHER = "WEATHER"
    GAME = "GAME"
    GAME_ACTION = "GAME_ACTION"
    GAME_ADVENTURE = "GAME_ADVENTURE"
    GAME_ARCADE = "GAME_ARCADE"
    GAME_BOARD = "GAME_BOARD"
    GAME_CARD = "GAME_CARD"
    GAME_CASINO = "GAME_CASINO"
    GAME_CASUAL = "GAME_CASUAL"
    GAME_EDUCATIONAL = "GAME_EDUCATIONAL"
    GAME_MUSIC = "GAME_MUSIC"
    GAME_PUZZLE = "GAME_PUZZLE"
    GAME_RACING = "GAME_RACING"
    GAME_ROLE_PLAYING = "GAME_ROLE_PLAYING"
    GAME_SIMULATION = "GAME_SIMULATION"
    GAME_SPORTS = "GAME_SPORTS"
    GAME_STRATEGY = "GAME_STRATEGY"
    GAME_TRIVIA = "GAME_TRIVIA"
    GAME_WORD = "GAME_WORD"
    FAMILY = "FAMILY"


class Collection(StrEnum):
    TOP_FREE = "topselling_free"
    TOP_PAID = "topselling_paid"
    GROSSING = "topgrossing"
    TRENDING = "movers_shakers"
    TOP_FREE_GAMES = "topselling_free_games"
    TOP_PAID_GAMES = "topselling_paid_games"
    TOP_GROSSING_GAMES = "topselling_grossing_games"
    NEW_FREE = "topselling_new_free"
    NEW_PAID = "topselling_new_paid"
    NEW_FREE_GAMES = "topselling_new_free_games"
    NEW_PAID_GAMES = "topselling_new_paid_games"


class Sort(IntEnum):
    NEWEST = 2
    RATING = 3
    HELPFULNESS = 1


class Age(StrEnum):
    FIVE_UNDER = "AGE_RANGE1"
    SIX_EIGHT = "AGE_RANGE2"
    NINE_UP = "AGE_RANGE3"


class Permission(IntEnum):
    COMMON = 0
    OTHER = 1


class GPlay:
    cluster = Cluster
    language = Language
    country = Country
    category = Category
    collection = Collection
    sort = Sort
    age = Age
    permission = Permission

    def __init__(self, base_url: str = "https://play.google.com") -> None:
        self._base_url = base_url

    async def _request_batchexecute(
        self, params: dict[str, Any], headers: dict[str, Any], data: Any
    ):
        # TODO: async
        response = requests.post(
            f"{self._base_url}/_/PlayStoreUi/data/batchexecute",
            params=params,
            # cookies=cookies,
            headers=headers,
            data=data,
        )

        return response

    async def _request_top(
        self,
        collection: str,
        category: str,
        language: str,
        length: int,
    ):
        inner = json.dumps(
            [
                [
                    None,
                    [[None, [None, length]], None, None, [113]],
                    [2, collection, category],
                ]
            ]
        )

        data = f"f.req={json.dumps([[['vyAe2', inner]]])}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            # 'Accept-Encoding': 'gzip, deflate, br',
            "Referer": "https://play.google.com/",
            "X-Same-Domain": "1",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Origin": "https://play.google.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "DNT": "1",
            "Sec-GPC": "1",
        }

        params = {
            "rpcids": "vyAe2",
            "source-path": "/store/apps",
            "f.sid": "3985578500523740800",
            "bl": "boq_playuiserver_20230314.03_p0",
            "hl": language,
            "authuser": "0",
            "_reqid": "68744",
        }

        return await self._request_batchexecute(
            params=params, headers=headers, data=data
        )

    async def _parse_response(self, content: str) -> list[ChartApplication]:
        try:
            app_entries = content[0][1][0][28][0]
        except Exception:
            return []
        apps = []
        for _, app_data in enumerate(app_entries):
            data = app_data[0]

            app = ChartApplication(
                id=data[0][0],
                # icon_url=data[1][3][2],
                # screenshot_urls=[i[3][2] for i in data[2]],
                # name=data[3],
                # rating=data[4][1],
                # category=data[5],
                # price=f"{data[8][1][0][0] / 1e6} {data[8][1][0][1]}",
                # buy_url=data[8][6][5][2],
                # store_path=data[10][4][2],
                # trailer_url=data[12][0][0][3][2] if data[12] else None,
                # description=data[13][1],
                # developer=data[14],
                # downloads=data[15],
                # cover_image_url=data[22][3][2],
            )
            apps.append(app)
        return apps

    async def build_application_data(
        self, app_id: str, app_category: str, load_reviews: bool = True
    ) -> GPlayAppModel:
        """
        Builds application models and database objects

        Args:
            app_id (str): The app id on Google Play
            load_reviews (bool, optional): Whether to also load the reviews of the application. Defaults to True.

        Returns:
            GPlayAppModel: A data model of the Application
        """

        import google_play_scraper

        logger.debug(f"Loading information for app {app_id}")

        try:
            app_ = google_play_scraper.app(app_id)
        except Exception:
            return None

        if "released" in app_ and app_['released'] is not None:
            app_["released"] = datetime.strptime(app_["released"], "%b %d, %Y")
        if "updated" in app_ and app_['updated'] is not None:
            app_["updated"] = datetime.fromtimestamp(app_["updated"])

        print(str(app_category))
        app = GPlayAppModel(**app_, app_category=str(app_category))

        async with SessionLocal() as session:
            await create_db_obj(db_session=session, model_class=GPlayApp, obj=app)

            if load_reviews:
                logger.info(
                    f"Begin loading reviews for {app.app_id} from Google Play, this may take some time..."
                )
                async for reviews in app.reviews_all():
                    logger.info(f"{len(reviews)}")
                    reviews = [
                        GPlayReviewModel(app_id=app.app_id, **review) for review in reviews
                    ]

                    for review in reviews:
                        await create_db_obj(
                            db_session=session, model_class=GPlayReview, obj=review
                        )
                logger.info(f"End loading reviews for {app.app_id}")
        
        return app

    async def fetch_top_charts(
        self,
        collection: str,
        category: str,
        language: str,
        length: int = 50,
        load_reviews: bool = True,
    ) -> list[GPlayAppModel]:
        """
        Fetches the top apps from the specified collection and category

        Args:
            collection (str): The collection, from gplay.collection
            category (str): The category, from gplay.category
            language (str): The language, from gplay.language
            length (int, optional): The length to pull from top charts, maxes at 660 due to API limitations. Defaults
            to 50.

        Returns:
            list[GPlayAppModel]: A list of the found applications in the top charts
        """

        response = await self._request_top(
            collection=collection, category=category, language=language, length=length
        )

        response_content = response.text

        content = json.loads(response_content.split("\n")[2])

        response_content = content[0][2]
        json_content = json.loads(response_content)

        apps = await self._parse_response(json_content)

        models = []
        async with SessionLocal() as session:
            for app in apps:
                if app is not None:
                    result = await session.execute(
                        select(GPlayApp).where(GPlayApp.app_id == app.app_id)
                    )
                    db_obj = result.scalars().first()

                    if db_obj:
                        logger.info(f"App {app.app_id} already processed, skipping")
                        continue
                    models.append(await self.build_application_data(app.app_id, app_category=category, load_reviews=load_reviews))
        return models

    async def fetch_similar(self, app: GPlayAppModel) -> list[GPlayAppModel]:
        """
        Fetches similar apps to the specified app

        Args:
            app (GPlayAppModel): The app data model

        Returns:
            list[GPlayAppModel]: A list of similar apps to the original app
        """

        resp = requests.get(self._base_url + await app.similar_cluster())

        soup = BeautifulSoup(resp.text, "lxml")

        apps = []
        for a in soup.find_all("a"):
            if "/store/apps/details?id=" in a["href"]:
                app_id = a["href"].replace("/store/apps/details?id=", "")

                apps.append(await self.build_application_data(app_id=app_id))
        return apps

    async def fetch_all(self, load_reviews: bool):
        """
        Fetches all apps from all categories and collections
        """
        for collection in self.collection:
            for category in self.category:
                length = 250
                logger.info(
                    f"Extracting top {length} from {collection} / {category} with language {self.language.EN}"
                )
                apps = await self.fetch_top_charts(
                    collection=collection,
                    category=category,
                    language=self.language.EN,
                    length=length,
                    load_reviews=load_reviews,
                )

                logger.info(f"Found {len(apps)} apps")

    async def fetch_all_recursive(self, load_reviews: bool):
        """
        Fetches all apps from all categories and collections, along with recursively descending similar apps to all
        apps. Should be a fairly exhaustive search.
        """

        async with SessionLocal() as session:
            to_search_similar = []
            gp = GPlay()
            for collection in gp.collection:
                for category in gp.category:
                    length = 250
                    logger.info(
                        f"Extracting top {length} from {collection} / {category} with language {gp.language.EN}"
                    )
                    apps = await self.fetch_top_charts(
                        collection=collection,
                        category=category,
                        language=self.language.EN,
                        length=length,
                        load_reviews=load_reviews
                    )

                    logger.info(f"Found {len(apps)} apps")

                    to_search_similar.append([app.app_id for app in apps])
                    while len(to_search_similar) > 0:
                        app = to_search_similar.pop()

                        result = await session.execute(
                            select(GPlayApp).where(GPlayApp.app_id == app.app_id)
                        )
                        db_obj = result.scalars().first()

                        if db_obj:
                            logger.info(f"App {app.app_id} already processed, skipping")
                            continue

                        logger.info(f"Finding similar apps to {app.app_id}")
                        similar_apps = await self.fetch_similar(app)
                        logger.info(
                            f"Found {len(similar_apps)} similar apps to {app.app_id}"
                        )
                        to_search_similar.append([app.app_id for app in similar_apps])
                        await asyncio.sleep(15)
