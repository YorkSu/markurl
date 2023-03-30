# -*- coding: utf-8 -*-
"""
Git Handlers

Including GithubRepoHandler.

- GithubRepoHandler match GitHub repo url

"""

import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from markurl.handler.model import Info, Handler
from markurl.util import SESS, clear_str, cfg

logger = logging.getLogger('markurl')


class GithubRepoHandler(Handler):
    _pattern = r"(?:https?://)?github\.com/[^/]+/[^/]+"

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        search = re.findall(cls._pattern, url)
        return cls.get_info(search[0]) if len(search) else None

    @classmethod
    def get_info(cls, url: str) -> Optional[Info]:
        try:
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            title = soup.find("strong", {"class": "mr-2 flex-self-stretch"}).text
            author = soup.find("span", {"class": "author"}).text
            return Info(
                type='Repo',
                title=clear_str(title),
                author=clear_str(author),
                source='GitHub',
                url=url
            )
        except Exception:
            logger.exception(f"Web page: {url} error")

        return None


handlers = (
    GithubRepoHandler,
)



