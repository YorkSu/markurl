"""
arXiv API
1. Get HTML content from arxiv URL
2. Output Markdown format: `title, first author, 'arXiv', year, URL`
"""

import re
from urllib.parse import quote
from unidecode import unidecode

from bs4 import BeautifulSoup
import feedparser

from markurl.util import get_html


def get_arxiv_info(url: str):
    """
    Get arxiv info from url
    """
    # html = requests.get(url).text
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(get_html(url), 'html.parser')
    title = re.sub('Title:', '', soup.find('h1', {'class': 'title mathjax'}).text.strip())
    authors = re.sub('Authors:', '', soup.find('div', {'class': 'authors'}).text.strip())
    first_author = authors.split(',')[0]
    year = soup.find('div', {'class': 'dateline'}).text.strip()
    year = re.search(r'\d{4}', year).group()
    return {
        'title': title,
        'first_author': first_author,
        'journal': 'arXiv',
        'year': year,
        'url': url,
        'citations': None,
    }


class ArxivAdapter(object):
    base_url = "http://export.arxiv.org/api/query?search_query={}:{}"

    def get_info(self, url: str):
        infos = feedparser.parse(url)['entries'][0]
        return {
            'title': infos['title'],
            'author': infos['author'],
            'journal': 'arXiv',
            'year': infos['published_parsed'][0],
            'url': infos['link'],
            'pdf': re.sub('abs', 'pdf', infos['link']),
            'citations': None,
        }

    def get_info_by_id(self, arxiv_id: str) -> dict:
        try:
            url = self.base_url.format('id', arxiv_id)
            return self.get_info(url)
        except:
            print(f"DOI: {arxiv_id} is error")

    def get_info_by_title(self, title: str) -> dict:
        try:
            url = self.base_url.format('ti', quote(unidecode(title)))
            return self.get_info(url)
        except:
            print(f"Title: {title} not found")
