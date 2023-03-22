# -*- coding: utf-8 -*-
"""
Zhihu Handlers

Including AnswerHandler.

- AnswerHandler match Zhihu question and answer url

"""

import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from markurl.handler.model import Info, Handler
from markurl.util import SESS, clear_str

logger = logging.getLogger('markurl')


class AnswerHandler(Handler):
    base_url = "https://www.zhihu.com/question/{q}/answer/{a}"
    _pattern = r"(?:https?://)?(?:www\.)?zhihu\.com/question/(.*)/answer/(.*)"

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        qna = cls.get_qna(url)

        if qna:
            return cls.get_info(*qna)

        return None

    @classmethod
    def get_qna(cls, url: str) -> (str, str):
        search = re.findall(cls._pattern, url)
        return search[0] if len(search) else ''

    @classmethod
    def get_info(cls, q: str, a: str) -> Optional[Info]:
        url = cls.base_url.format(q=q, a=a)

        try:
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            question = soup.find("h1", {"class": "QuestionHeader-title"}).text
            author = soup.find("span", {"class": "UserLink AuthorInfo-name"}).text.strip('\u200b')
            date = soup.find("div", {"class": "ContentItem-time"})\
                .find_all("span")[0].text.strip().split(' ')[1]

            return Info(
                type='Answer',
                title=clear_str(question),
                author=clear_str(author),
                source='知乎',
                date=clear_str(date),
                url=url
            )
        except Exception:
            logger.exception(f"Zhihu Q&A: {url} not found")

        return None


class ZhuanlanHandler(Handler):
    base_url = "https://zhuanlan.zhihu.com/p/{page}"
    _pattern = r"(?:https?://)?zhuanlan\.zhihu\.com/p/(.*)"

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        page = cls.get_page(url)

        if page:
            return cls.get_info(page)

        return None

    @classmethod
    def get_page(cls, url: str) -> str:
        search = re.findall(cls._pattern, url)
        return search[0] if len(search) else ''

    @classmethod
    def get_info(cls, page: str) -> Optional[Info]:
        url = cls.base_url.format(page=page)

        try:
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            title = soup.find("h1", {"class": "Post-Title"}).text
            author = soup.find_all("a", {"class": "UserLink-link"})[1].text
            date = soup.find("div", {"class": "ContentItem-time"}) \
                .text.strip().split(' ')[1]

            return Info(
                type='Article',
                title=clear_str(title),
                author=clear_str(author),
                source='知乎',
                date=clear_str(date),
                url=url
            )
        except Exception:
            logger.exception(f"Zhihu Zhuanlan: {url} not found")

        return None


handlers = (
    AnswerHandler,
    ZhuanlanHandler,
)
