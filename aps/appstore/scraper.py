import logging
import random
import re
import sys
import time
from datetime import datetime

import requests

logger = logging.getLogger("Base")


# Pulled from app-store-scraper, as that does not work with the project setup
# Unused


class Base:
    _scheme = "https"

    _landing_host = ""
    _request_host = ""

    _landing_path = ""
    _request_path = ""

    _user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    ]

    def __init__(
        self,
        country,
        app_name,
        app_id,
    ):
        self._base_landing_url = f"{self._scheme}://{self._landing_host}"
        self._base_request_url = f"{self._scheme}://{self._request_host}"

        self._country = str(country).lower() or "us"
        self._app_name = re.sub(r"[\W_]+", "-", str(app_name).lower())
        self._app_id = int(app_id)

        self._request_headers = {
            "Accept": "application/json",
            "Authorization": self._token(self._landing_url),
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self._base_landing_url,
            "Referer": self._landing_url,
            "User-Agent": random.choice(self._user_agents),
        }
        self._request_params = {}
        self._response = requests.Response()

        logger.info(
            f"Initialised: {self.__class__.__name__}"
            f"('{self._country}', '{self._app_name}', {self._app_id})"
        )
        logger.info(f"Ready to fetch reviews from: {self._landing_url}")

    @property
    def _landing_url(self):
        landing_url = f"{self._base_landing_url}/{self._landing_path}"
        return landing_url.format(
            country=self._country, app_name=self._app_name, app_id=self._app_id
        )

    @property
    def _request_url(self):
        request_url = f"{self._base_request_url}/{self._request_path}"
        return request_url.format(country=self._country, app_id=self._app_id)

    def _get(
        self,
        url,
        headers=None,
        params=None,
        total=3,
        backoff_factor=3,
        status_forcelist=[404, 429],
    ) -> requests.Response:
        # retries = Retry(
        #     total=total,
        #     backoff_factor=backoff_factor,
        #     status_forcelist=status_forcelist,
        # )
        resp = requests.get(url, headers=headers, params=params)

        if resp.status_code == 429:
            print(resp)
        return resp

    def _token(self, url):
        resp = self._get(url)
        tags = resp.text.splitlines()
        for tag in tags:
            if re.match(r"<meta.+web-experience-app/config/environment", tag):
                token = re.search(r"token%22%3A%22(.+?)%22", tag).group(1)
                return f"bearer {token}"

    def _parse_data(self, response, after):
        response = response.json()
        reviews = []
        for i, data in enumerate(response["data"]):
            review = data["attributes"]
            review["date"] = datetime.strptime(review["date"], "%Y-%m-%dT%H:%M:%SZ")
            if after and review["date"] < after:
                continue
            reviews.append(review)
            logger.debug(f"Fetched {i} review(s)")
        return reviews

    def _parse_next(self, response: requests.Response):
        next_offset = response.json().get("next")
        if next_offset is None:
            request_offset = None
        else:
            offset = re.search("^.+offset=([0-9]+).*$", next_offset).group(1)
            request_offset = int(offset)
        return request_offset

    def review(self, how_many=sys.maxsize, after=None, sleep: int = 5):
        if after and not isinstance(after, datetime):
            raise SystemExit("`after` must be a datetime object.")
        reviews_all = []
        try:
            while True:
                resp = self._get(
                    self._request_url,
                    headers=self._request_headers,
                    params=self._request_params,
                )
                reviews_all.extend(self._parse_data(resp, after))
                request_offset = self._parse_next(resp)
                if request_offset is None or len(reviews_all) >= how_many:
                    break
                else:
                    self._request_params.update({"offset": request_offset})
                if sleep and type(sleep) is int:
                    time.sleep(sleep)
        except KeyboardInterrupt:
            logger.error("Keyboard interrupted")
        except Exception as e:
            logger.error(f"Something went wrong: {e}")
        finally:
            return reviews_all


class AppStore(Base):
    _landing_host = "apps.apple.com"
    _request_host = "amp-api.apps.apple.com"

    _landing_path = "{country}/app/{app_name}/id{app_id}"
    _request_path = "v1/catalog/{country}/apps/{app_id}/reviews"

    def __init__(
        self,
        country,
        app_name,
        app_id=None,
    ):
        super().__init__(
            country=country,
            app_name=app_name,
            app_id=app_id,
        )

        # override
        self._request_params = {
            "l": "en-GB",
            "offset": 0,
            "limit": 20,
            "platform": "web",
            "additionalPlatforms": "appletv,ipad,iphone,mac",
        }
