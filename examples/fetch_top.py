from aps.gplay import GPlay

gplay = GPlay()

gplay.fetch_top_charts(chart=GPlay.charts.TOP_FREE, category="APPLICATION")

print()
