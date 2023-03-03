"""
Crossref API

Get info by DOI or title using Crossref api
"""

import re
import logging
from urllib.parse import quote
from unidecode import unidecode

from markurl.util import SESS, quote_url


logger = logging.getLogger('markurl')


class CrossrefAdapter(object):
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
        
        journal = 'No journal'
        if 'short-container-title' in infos and len(infos['short-container-title']):
            journal = infos['short-container-title'][0]
        elif 'container-title' in infos and len(infos['container-title']):
            journal = infos['container-title'][0]
        
        return {
            'title': infos['title'][0],
            'author': first_author,
            'journal': journal,
            'year': infos['published']['date-parts'][0][0],
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
            print(e)
            print(f"DOI: {doi} not found")

    @classmethod
    def get_info_by_title(cls, title: str) -> dict:
        try:
            url = cls.base_url.format(f'?query.bibliographic={quote_url(title)}&rows=20')
            infos = SESS.get(url).json()["message"]
            for item in infos['items']:
                if item['title'][0].lower() == title.lower():
                    return cls.get_info(item)
        except Exception as e:
            print(e)
            print(f"Title: {title} not found")

    @classmethod
    def get_info_by_url(cls, url: str) -> dict:
        try:
            doi = re.findall('10[.][0-9]{4,}(?:[.][0-9]+)*\/[^\s]+', url)[0]
            return cls.get_info_by_id(doi)
        except:
            print(f"URL: {url} not found")
