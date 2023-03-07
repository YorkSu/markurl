"""
Utils
"""
import logging
import re
from urllib.parse import quote

import requests
from requests import Response
from unidecode import unidecode

logging.basicConfig()
logger = logging.getLogger('markurl')
logger.setLevel(logging.DEBUG)


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}
SESS = requests.Session()
SESS.headers = HEADERS
# SESS.proxies = {'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}


def get_html(url: str) -> Response:
    """
    Get HTML content from arxiv URL
    """
    try:
        r = SESS.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except Exception:
        logger.exception(f"Error: failed to get HTML content from {url}")


def quote_url(url: str) -> str:
    return quote(unidecode(url))


def clear_str(s: str) -> str:
    return re.sub(r"\n", '', s).strip()
