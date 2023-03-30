# -*- coding: utf-8 -*-
"""
Webpage Handlers

Including WebpageHandler.

- WebpageHandler match all url

"""

import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from markurl.handler.model import Info, Handler
from markurl.util import SESS, clear_str, cfg

logger = logging.getLogger('markurl')


DOMAIN_MAP = cfg.get('domain', {}).get('map', {})


class WebpageHandler(Handler):
    d_pattern = r"(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        return cls.get_info(url)

    @classmethod
    def get_info(cls, url: str) -> Optional[Info]:
        try:
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            title = soup.find("h1")
            if title:
                title = title.text
            if title is None:
                title = soup.find('meta', property='og:title')['content']

            source = re.findall(cls.d_pattern, url)[0]
            # extract domain
            domain_parts = source.split('.')
            domain = f"{domain_parts[-2]}.{domain_parts[-1]}"
            source = DOMAIN_MAP.get(domain, source)

            return Info(
                type='Page',
                title=clear_str(title),
                source=source,
                url=url
            )
        except Exception:
            logger.exception(f"Web page: {url} error")

        return None


handlers = (
    WebpageHandler,
)
