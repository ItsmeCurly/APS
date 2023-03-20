from google_play_scraper import reviews_all


result = reviews_all(
    "com.fantome.penguinisle",
    sleep_milliseconds=5,
)

print(result)
