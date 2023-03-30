# -*- coding: utf-8 -*-
"""
Douban Handlers

Including DoubanHandler.

- DoubanReviewHandler match Douban Review url

"""

import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from markurl.handler.model import Info, Handler
from markurl.util import SESS, clear_str

logger = logging.getLogger('markurl')


class DoubanReviewHandler(Handler):
    _pattern = r'(?:https?://)?movie\.douban\.com/review/\d+/?'

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        search = re.findall(cls._pattern, url)
        return cls.get_info(search[0]) if len(search) else None

    @staticmethod
    def get_info(url: str) -> Optional[Info]:
        try:
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            title = soup.find("h1").text
            date = soup.find("span", {"class": "main-meta"})
            if date is not None:
                date = date.text.split(' ')[0]
            return Info(
                type='Review',
                title=clear_str(title),
                date=date,
                source='豆瓣',
                url=url
            )
        except Exception:
            logger.exception(f"Douban Review: {url} error")

        return None


handlers = (
    DoubanReviewHandler,
)
