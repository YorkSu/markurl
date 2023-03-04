"""
arXiv API

Get info by arXiv_ID or title using arxiv api
"""

import re
import logging

from bs4 import BeautifulSoup
import feedparser

from markurl.adapter.adapter import Adapter
from markurl.util import get_html, quote_url


logger = logging.getLogger('markurl')


class ArxivAdapter(Adapter):
    base_url = "http://export.arxiv.org/api/query?search_query={}:{}"

    @staticmethod
    def get_info(infos: dict) -> dict:
        return {
            'type': 'Paper',
            'title': infos['title'],
            'author': infos['author'],
            'source': 'arXiv',
            # 'year': infos['published_parsed'][0],
            'year': infos['published'].split('T')[0],
            'url': infos['link'],
            'pdf': re.sub('abs', 'pdf', infos['link']),
            'citations': None,
        }

    @classmethod
    def get_info_by_id(cls, arxiv_id: str) -> dict:
        try:
            arxiv_id = re.findall('\d{4}\.\d{5}', arxiv_id)[0]
            url = cls.base_url.format('id', arxiv_id)
            infos = feedparser.parse(url)['entries'][0]
            # logger.info(infos)
            return cls.get_info(infos)
        except:
            logging.warning(f"DOI: {arxiv_id} not found")

    @classmethod
    def get_info_by_title(cls, title: str) -> dict:
        try:
            url = cls.base_url.format('ti', quote_url(title))
            infos = {}
            for item in feedparser.parse(url)['entries']:
                if re.match(f".*{title.lower()}.*", item['title'].lower()) is not None:
                    infos = item
                    break
            return cls.get_info(infos)
        except:
            logging.warning(f"Title: {title} not found")

    @classmethod
    def get_info_by_url(cls, url: str) -> dict:
        try:
            soup = BeautifulSoup(get_html(url), 'html.parser')
            title = re.sub('Title:', '', soup.find(
                'h1', {'class': 'title mathjax'}).text.strip())
            authors = re.sub('Authors:', '', soup.find(
                'div', {'class': 'authors'}).text.strip())
            first_author = authors.split(',')[0]
            year = soup.find('div', {'class': 'dateline'}).text.strip()
            year = re.search(r'\d{4}', year).group()
            return {
                'type': 'Paper',
                'title': title,
                'author': first_author,
                'source': 'arXiv',
                'year': year,
                'url': url,
                'pdf': re.sub('abs', 'pdf', url),
                'citations': None,
            }
        except:
            logging.warning(f"URL: {url} not found")
