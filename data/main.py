import random
import os
import typing as t

from dotenv import load_dotenv
from newsapi import NewsApiClient


load_dotenv()
client = NewsApiClient(api_key=os.getenv('NEWSAPI_KEY'))
SOURCES_LIMIT: int = 10
TApiReponse = dict[str, str | list[str]]


def _parse_response(response: TApiReponse):
    pass


sources_response = client.get_sources()
sources: list[TApiReponse] = sources_response.get('sources')
if sources:
    article_responses: list[TApiReponse] = [
        client.get_everything(sources=source['id']) for source in random.suffle(sources)[:SOURCES_LIMIT]
    ]
