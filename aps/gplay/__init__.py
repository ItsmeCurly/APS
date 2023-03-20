import json
from typing import Any
import requests

from aps.gplay.application.models import ChartApplication


class Charts:
    TOP_FREE = "topselling_free"
    TOP_GROSS = "topgrossing"
    TOP_SELL = "topselling_paid"


class GPlay:
    charts = Charts()

    def __init__(self, base_url: str = "https://play.google.com") -> None:
        self._base_url = base_url

    def _request(self, params: dict[str, Any], headers: dict[str, Any], data: Any):
        response = requests.post(
            f"{self._base_url}/_/PlayStoreUi/data/batchexecute",
            params=params,
            # cookies=cookies,
            headers=headers,
            data=data,
        )

        return response

    def _request_top(
        self,
        chart: str,
        category: str,
        length: int,
    ):
        inner = json.dumps(
            [[None, [[None, [None, length]], None, None, [113]], [2, chart, category]]]
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
            "hl": "en",
            "authuser": "0",
            "_reqid": "68744",
        }

        return self._request(params=params, headers=headers, data=data)

    def _parse_response(self, content: str):
        app_entries = content[0][1][0][28][0]
        apps = []
        for app_num, app_data in enumerate(app_entries):
            data = app_data[0]

            app = ChartApplication(
                id=data[0][0],
                icon_url=data[1][3][2],
                screenshot_urls=[i[3][2] for i in data[2]],
                name=data[3],
                rating=data[4][1],
                category=data[5],
                price=f"{data[8][1][0][0] / 1e6} {data[8][1][0][1]}",
                buy_url=data[8][6][5][2],
                store_path=data[10][4][2],
                trailer_url=data[12][0][0][3][2] if data[12] else None,
                description=data[13][1],
                developer=data[14],
                downloads=data[15],
                cover_image_url=data[22][3][2],
            )
            print(app)
            apps.append(app)
        return apps

    def fetch_top_charts(
        self,
        chart: str,
        category: str,
        length: int = 50,
    ):
        response = self._request_top(chart=chart, category=category, length=length)

        response_content = response.text

        content = json.loads(response_content.split("\n")[2])

        response_content = content[0][2]
        json_content = json.loads(response_content)

        return self._parse_response(json_content)
