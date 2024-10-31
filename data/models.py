import datetime as dt

from pydantic import BaseModel


class Article(BaseModel):
    source: str
    author: str
    title: str
    description: str
    url: str
    url_to_image: str
    published_at: dt.datetime
