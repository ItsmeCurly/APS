from pydantic import BaseModel
from sqlalchemy import Column, Integer

from aps.db.models.base import Base




class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True, index=True)




class ApplicationBase(BaseModel):
    id: str

    def reviews(self):
        from google_play_scraper import reviews_all

        return reviews_all(app_id=self.id, sleep_milliseconds=5000)

class ChartApplication(ApplicationBase):
    id: str
    icon_url: str
    screenshot_urls: list[str]
    name: str
    rating: float
    category: str
    price: str
    buy_url: str
    store_path: str
    trailer_url: str | None = None
    description: str
    developer: str
    downloads: str
    cover_image_url: str
