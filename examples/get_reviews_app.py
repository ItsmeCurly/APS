from google_play_scraper import reviews_all, Sort


result = reviews_all(
    'com.fantome.penguinisle',
    sleep_milliseconds=5,
)

print(result)