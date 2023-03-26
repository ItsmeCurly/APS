import asyncio
from aps.gplay import GPlay

gplay = GPlay()

asyncio.run(gplay.fetch_all_recursive())
