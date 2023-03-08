# -*- coding: utf-8 -*-
"""
Paper Adapters

Including ArxivAdapter, CrossrefAdapter and TitleAdapter.

- ArxivAdapter match arXiv id
- CrossrefAdapter match DOI
- TitleAdapter will first perform an exact match in Crossref,
  and if not, match in arXiv

"""
import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from markurl.adapter.model import Info, Adapter
from markurl.util import SESS, quote_url, clear_str

logger = logging.getLogger('markurl')


class ArxivAdapter(Adapter):
    base_url = "http://export.arxiv.org/api/query?search_query=id:{}"

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        arxiv_id = cls.get_id(url)
        if arxiv_id:
            return cls.get_info_by_id(arxiv_id)

        return None

    @staticmethod
    def get_id(url: str) -> str:
        id_pattern = r'^(\d{4}\.\d{4,5})(?:v\d+)?'
        url_pattern = r'arxiv\.org\/(?:abs|pdf)\/(\d{4}\.\d{4,5})(?:v\d+)?'

        id_search = re.findall(id_pattern, url)
        url_search = re.findall(url_pattern, url)

        if len(id_search):
            return id_search[0]
        if len(url_search):
            return url_search[0]

        return ''

    @classmethod
    def get_info_by_id(cls, arxiv_id: str) -> Optional[Info]:
        try:
            url = cls.base_url.format(arxiv_id)
            soup = BeautifulSoup(SESS.get(url).text, 'lxml-xml')
            entry = soup.find_all('entry')[0]
            return cls.get_info_from_entry(entry)
        except Exception:
            logger.exception(f"arXiv ID: {arxiv_id} not found")

        return None

    @staticmethod
    def get_info_from_entry(entry: BeautifulSoup) -> Info:
        title = entry.find_all('title')[0].text
        author = entry.find_all('author')[0].text
        date = entry.find_all('published')[0].text.split('T')[0]
        link = entry.find_all('link')[0]['href']
        pdf = entry.find_all('link')[1]['href']
        return Info(
            type='Paper',
            title=clear_str(title),
            author=clear_str(author),
            source='arXiv',
            date=clear_str(date),
            url=clear_str(link),
            pdf=clear_str(pdf),
        )


class CrossrefAdapter(Adapter):
    base_url = "http://api.crossref.org/works/{}"

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        doi = cls.get_id(url)
        if doi:
            return cls.get_info_by_doi(doi)

        return None

    @staticmethod
    def get_id(url: str) -> str:
        id_pattern = r'(10[.][0-9]{4,}(?:[.][0-9]+)*\/[^\s]+)'
        id_search = re.findall(id_pattern, url)

        if len(id_search):
            return id_search[0]

        return ''

    @classmethod
    def get_info_by_doi(cls, doi: str) -> Optional[Info]:
        try:
            url = cls.base_url.format(doi)
            item = SESS.get(url).json()["message"]
            return cls.get_info_from_item(item)
        except Exception:
            logger.exception(f"DOI: {doi} not found")

    @staticmethod
    def get_info_from_item(item: dict) -> Optional[Info]:
        first_author = None
        if 'author' in item:
            for author in item['author']:
                if author['sequence'] == 'first':
                    first_author = ' '.join([
                        author['family'],
                        author['given']
                    ])

        source = 'No journal'
        if 'short-container-title' in item and len(item['short-container-title']):
            source = item['short-container-title'][0]
        elif 'container-title' in item and len(item['container-title']):
            source = item['container-title'][0]

        return Info(
            type='Paper',
            title=clear_str(item['title'][0]),
            author=first_author,
            source=clear_str(source),
            date='-'.join(map(
                str,
                item['published']['date-parts'][0]
            )),
            url=clear_str(item['URL']),
            pdf=clear_str(item['link'][0]['URL']),
            citations=str(item['is-referenced-by-count']),
        )


class TitleAdapter(Adapter):
    arxiv_url = "http://export.arxiv.org/api/query?search_query=ti:{}"
    crossref_url = "http://api.crossref.org/works?query.bibliographic={}&rows=20"

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        return (cls.get_info_from_crossref(url)
                or cls.get_info_from_arxiv(url))

    @classmethod
    def get_info_from_arxiv(cls, query: str) -> Optional[Info]:
        try:
            url = cls.arxiv_url.format(quote_url(query))
            soup = BeautifulSoup(SESS.get(url).text, 'lxml-xml')
            for entry in soup.find_all('entry'):
                title = entry.find_all('title')[0].text.strip()
                if re.search(f"{query.lower()}", title.lower()):
                    return ArxivAdapter.get_info_from_entry(entry)
        except Exception:
            logger.exception(f"arXiv Title: {query} not found")

        return None

    @classmethod
    def get_info_from_crossref(cls, query: str) -> Optional[Info]:
        try:
            url = cls.crossref_url.format(quote_url(query))
            resp = SESS.get(url).json()['message']
            for item in resp['items']:
                if item['title'][0].lower() == query.lower():
                    return CrossrefAdapter.get_info_from_item(item)
        except Exception:
            logger.exception(f"Crossref Title: {query} not found")

        return None


adapters = (
    ArxivAdapter,
    CrossrefAdapter,
    TitleAdapter,
)
