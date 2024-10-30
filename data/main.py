import os

from dotenv import load_dotenv
from newsapi import NewsApiClient


load_dotenv()
client = NewsApiClient(api_key=os.getenv('NEWSAPI_KEY'))
SOURCES_LIMIT: int = 10
TApiReponse = dict[str, str | list[str]]


def _parse_response(response: TApiReponse) -> list[TApiReponse] | None:
    status = response.get('status')
    if not status or status != 'ok':
        return
    else:
        articles = response.get('articles')
        if not articles:
            return
        else:
            articles.pop('content')
            return articles


sources_response = client.get_sources()
sources: list[TApiReponse] = sources_response.get('sources')
if sources:
    article_responses: list[TApiReponse] = [
        client.get_everything(sources=source['id']) for source in sources[:SOURCES_LIMIT]
    ]
