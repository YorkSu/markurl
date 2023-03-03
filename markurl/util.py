"""
Utils
"""


import requests
from urllib.parse import quote
from unidecode import unidecode


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}
SESS = requests.Session()
SESS.headers = HEADERS
SESS.proxies = {'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}


def get_html(url: str) -> str:
    """
    Get HTML content from arxiv URL
    """
    try:
        r = SESS.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print(f"Error: failed to get HTML content from {url}")
        return ""


def quote_url(url: str) -> str:
    return quote(unidecode(url))


def info_to_markdown(info: dict) -> str:
    """
    Output Markdown format: `title, first author, journal, year, URL, citations`
    """
    pre_text = [
        info['title'],
        info['author'],
        info['journal'],
        info['year'],
        f"[URL]({info['url']})",
    ]
    if info['citations'] is not None:
        pre_text.append(info['citations'])
    return ", ".join([str(i) for i in pre_text])
