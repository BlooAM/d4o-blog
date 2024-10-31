import json
import os

from dotenv import load_dotenv
import inflection
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from pathlib import Path
from pydantic_core._pydantic_core import ValidationError as PydanticValidationError

from models import Article


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
    return resource


def parse_article(article: dict[str: str | dict]) -> Article:
    article_components = {
        inflection.underscore(article_entity): article.get(article_entity)
        for article_entity in article.keys()
    }
    article_parsed = Article(**article_components)
    return article_parsed


def parse_response(response: TApiReponse) -> list[Article] | None:
    status = response.get('status')
    if not status or status != 'ok':
        return
    else:
        articles = response.get('articles')
        parsed_articles = []
        for article in articles:
            try:
                parsed_article = parse_article(article)
                parsed_articles.append(parsed_article)
            except PydanticValidationError as e:
                print(f'Article could`t be parsed with the following exception: {e}')

        return parsed_articles


def fetch_sources(fetch_local_sources: bool = False) -> list[TApiReponse]:
    if fetch_local_sources:
        sources = _get_test_static_resource(resource_name='sample_sources')
    else:
        sources_response = client.get_sources()
        sources: list[TApiReponse] = sources_response.get('sources')

    return sources


def dump_data(articles: list[Article]) -> None:
    data_dir = CURR_DIR
    data_path = data_dir / 'data.json'
    data_objects = [article.json() for article in articles]
    with open(data_path, 'w') as fp:
        json.dump(fp, data_objects)


def main(save_results: bool = False):
    sources: TApiReponse = fetch_sources(fetch_local_sources=FETCH_LOCAL_SOURCES)
    article_responses: list[TApiReponse] = []
    for source in sources:
        try:
            article_response = client.get_everything(sources=source['id'])
            article_responses.append(article_response)
        except NewsAPIException as e:
            article_responses = _get_test_static_resource(resource_name='sample_articles_response')

        parsed_articles = parse_response(article_responses)
        if save_results:
            dump_data(articles=parsed_articles)
    return parsed_articles


if __name__ == '__main__':
    results = main(save_results=True)
