# -*- coding: utf-8 -*-
"""
Wiki Handlers

Including WikipediaHandler.

- WikipediaHandler match Wikipedia url

"""

import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from markurl.handler.model import Info, Handler
from markurl.util import SESS, clear_str

logger = logging.getLogger('markurl')


class WikipediaHandler(Handler):
    u_pattern = r'(?:https?://)?[^/]*\.wikipedia\.org/[^/]+/.+'

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        search = re.findall(cls.u_pattern, url)
        return cls.get_info(search[0]) if len(search) else None

    @staticmethod
    def get_info(url: str) -> Optional[Info]:
        try:
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            title = soup.find("h1").text
            return Info(
                type='Knowledge',
                title=clear_str(title),
                source='Wikipedia',
                url=url
            )
        except Exception:
            logger.exception(f"Wikipedia: {url} error")

        return None


handlers = (
    WikipediaHandler,
)
