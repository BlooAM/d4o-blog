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
FETCH_LOCAL_SOURCES = True
TApiReponse = dict[str, str | list[str]]


def _get_test_static_resource(resource_name: str) -> list[TApiReponse]:
    sample_data_dir = CURR_DIR / 'tests' / 'static'
    sample_data_path = sample_data_dir / f'{resource_name}.json'
    with open(sample_data_path, 'r') as fp:
        resource = json.load(fp)
    return  resource


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


def fetch_sources(fetch_local_sources: bool = False) -> list[TApiReponse]:
    if fetch_local_sources:
        sources = _get_test_static_resource(resource_name='sample_sources')
    else:
        sources_response = client.get_sources()
        sources: list[TApiReponse] = sources_response.get('sources')

    return sources


sources: TApiReponse = fetch_sources(fetch_local_sources=FETCH_LOCAL_SOURCES)
article_responses: list[TApiReponse] = []
for source in sources:
    try:
        article_response = client.get_everything(sources=source['id'])
        article_responses.append(article_response)
    except NewsAPIException as e:
        article_responses = _get_test_static_resource(resource_name='sample_articles_response')
