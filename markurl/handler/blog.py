# -*- coding: utf-8 -*-
"""
Blog Handlers

Including CSDNHandler.

- CSDNHandler match CSDN blog url

"""

import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from markurl.handler.model import Info, Handler
from markurl.util import SESS, clear_str, cfg

logger = logging.getLogger('markurl')


class CSDNHandler(Handler):
    _pattern = r"(?:https?://)?blog\.csdn\.net/[^/]+/article/details/[^/]+"

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        search = re.findall(cls._pattern, url)
        return cls.get_info(search[0]) if len(search) else None

    @classmethod
    def get_info(cls, url: str) -> Optional[Info]:
        try:
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            title = soup.find("h1").text
            author = soup.find("a", {"class": "follow-nickName"}).text
            date = soup.find("div", {"class": "bar-content"})\
                .find("span", {"class": "time"}).text\
                .replace(u'\xa0', ' ').split(' ')[1]
            return Info(
                type='Article',
                title=clear_str(title),
                author=clear_str(author),
                date=clear_str(date),
                source='CSDN',
                url=url
            )
        except Exception:
            logger.exception(f"Web page: {url} error")

        return None


handlers = (
    CSDNHandler,
)



