import json
import os

from dotenv import load_dotenv
import inflection
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from pathlib import Path


load_dotenv()
client = NewsApiClient(api_key=os.getenv('NEWSAPI_KEY'))
CURR_DIR = Path(__file__).parent
SOURCES_LIMIT: int = 2
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


try:
    sources_response = client.get_sources()
    sources: list[TApiReponse] = sources_response.get('sources')
except NewsAPIException as e:
    sample_data_dir = CURR_DIR / 'tests' / 'static'
    sample_data_path = sample_data_dir / 'sample_sources.json'
    with open(sample_data_path, 'r') as fp:
        sources = json.load(fp)


if sources:
    article_responses: list[TApiReponse] = [
        client.get_everything(sources=source['id']) for source in sources[:SOURCES_LIMIT]
    ]
    article_response = article_responses[0]
