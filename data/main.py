import os

from dotenv import load_dotenv
from newsapi import NewsApiClient


load_dotenv()
client = NewsApiClient(api_key=os.getenv('NEWSAPI_KEY'))

sources_response = client.get_sources()
sources = sources_response.get('sources')
if sources:
    article_responses = [client.get_everything(sources=source['id']) for source in sources[:10]]
