"""
Crossref API

Get info by DOI or title using Crossref api
"""

import re
import logging

from markurl.adapter.adapter import Adapter
from markurl.util import SESS, quote_url


logger = logging.getLogger('markurl')


class CrossrefAdapter(Adapter):
    base_url = "http://api.crossref.org/works{}"

    @staticmethod
    def get_info(infos: dict) -> dict:
        first_author = None
        if 'author' in infos:
            for author in infos['author']:
                if author['sequence'] == 'first':
                    first_author = ' '.join([
                        author['family'],
                        author['given']
                    ])
        
        source = 'No journal'
        if 'short-container-title' in infos and len(infos['short-container-title']):
            source = infos['short-container-title'][0]
        elif 'container-title' in infos and len(infos['container-title']):
            source = infos['container-title'][0]

        return {
            'type': 'Paper',
            'title': infos['title'][0],
            'author': first_author,
            'source': source,
            'year': '-'.join(map(
                str, 
                infos['published']['date-parts'][0]
            )),
            'url': infos['URL'],
            'pdf': infos['link'][0]['URL'],
            'citations': infos['is-referenced-by-count'],
        }

    @classmethod
    def get_info_by_id(cls, doi: str) -> dict:
        try:
            url = cls.base_url.format(f'/{doi}')
            infos = SESS.get(url).json()["message"]
            return cls.get_info(infos)
        except Exception as e:
            logging.warning(e)
            logging.warning(f"DOI: {doi} not found")

    @classmethod
    def get_info_by_title(cls, title: str) -> dict:
        try:
            url = cls.base_url.format(f'?query.bibliographic={quote_url(title)}&rows=20')
            infos = SESS.get(url).json()["message"]
            for item in infos['items']:
                if item['title'][0].lower() == title.lower():
                    return cls.get_info(item)
        except Exception as e:
            logging.warning(e)
            logging.warning(f"Title: {title} not found")

    @classmethod
    def get_info_by_url(cls, url: str) -> dict:
        try:
            doi = re.findall('10[.][0-9]{4,}(?:[.][0-9]+)*\/[^\s]+', url)[0]
            return cls.get_info_by_id(doi)
        except:
            logging.warning(f"URL: {url} not found")
