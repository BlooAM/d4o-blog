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


if FETCH_LOCAL_SOURCES:
    sources_response = client.get_sources()
    sources: list[TApiReponse] = sources_response.get('sources')
else:
    sample_data_dir = CURR_DIR / 'tests' / 'static'
    sample_data_path = sample_data_dir / 'sample_sources.json'
    with open(sample_data_path, 'r') as fp:
        sources = json.load(fp)


article_responses: list[TApiReponse] = []
if sources:
    for source in sources:
        try:
            article_response = client.get_everything(sources=source['id'])
            article_responses.append(article_response)
        except NewsAPIException as e:
            sample_data_dir = CURR_DIR / 'tests' / 'static'
            sample_data_path = sample_data_dir / 'sample_article_responses.json'
            with open(sample_data_path, 'r') as fp:
                article_reponses = json.load(fp)
