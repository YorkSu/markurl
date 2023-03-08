# -*- coding: utf-8 -*-
"""
Utils
"""
import logging
import re
from urllib.parse import quote

import requests
from requests import Response
from unidecode import unidecode

from markurl.config import Config


logging.basicConfig()
logger = logging.getLogger('markurl')
logger.setLevel(logging.DEBUG)
cfg = Config.load_config()
HEADERS = cfg.get('http', {}).get('headers', {})
PROXIES = cfg.get('http', {}).get('proxies', {})
SESS = requests.Session()
if HEADERS:
    SESS.headers = HEADERS
if PROXIES:
    SESS.proxies = PROXIES


def get_html(url: str) -> Response:
    """
    Get HTTP(S) Response from URL
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
