# -*- coding: utf-8 -*-
"""
Bilibili Handlers

Including BilibiliHandler.

- match bilibili (short) url
- match pure BVID
- match part Video
- match Bilibili Article
- match normal Video

"""

import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from markurl.handler.model import Info, Handler
from markurl.util import SESS, clear_str

logger = logging.getLogger('markurl')


class BilibiliHandler(Handler):
    base_url = 'https://www.bilibili.com/video/{bvid}'
    part_url = 'https://www.bilibili.com/video/{bvid}?p={part}'
    b_pattern = r'(?:https?://)?(?:www\.)?bilibili\.com/video/BV\S{10}'
    p_pattern = r'(?:https?://)?(?:www\.)?bilibili\.com/video/(BV\S{10})\?p=(\d+)'
    s_pattern = r'(?:https?://)?b23\.tv/.*'
    c_pattern = r'(?:https?://)?(?:www\.)?bilibili\.com/read/cv\d+'

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        # 短链接
        if re.match(cls.s_pattern, url):
            resp = SESS.get(url)
            url = resp.url

        # BVID
        if re.match(r'BV\S{10}', url):
            url = cls.base_url.format(bvid=url)

        # 分P视频
        search = re.findall(cls.p_pattern, url)
        if len(search):
            return cls.get_info_from_part(*search[0])

        # CV文章
        if re.match(cls.c_pattern, url):
            return cls.get_info_from_cv(url)

        # 普通视频
        search = re.findall(cls.b_pattern, url)
        if len(search):
            return cls.get_info(search[0])

        return None

    @staticmethod
    def get_info(url: str) -> Optional[Info]:
        try:
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            title = soup.find("h1", class_="tit").text
            author = soup.find("a", class_="username").text
            # 只取日期部分，去掉时间部分
            date = soup.find("span", class_="pudate-text").text.strip().split(" ")[0]
            link = soup.find("meta", property="og:url")['content']
            return Info(
                type='Video',
                title=clear_str(title),
                author=clear_str(author),
                source='Bilibili',
                date=clear_str(date),
                url=clear_str(link),
            )
        except Exception:
            logger.exception(f"Bilibili: `{url}` not found")

        return None

    @classmethod
    def get_info_from_part(cls, bvid: str, part: str) -> Optional[Info]:
        try:
            url = cls.part_url.format(bvid=bvid, part=part)
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            title = soup.find("h1", class_="tit").text
            # 获取分p标题
            part_title_ori = soup.find("meta", property="og:title")['content']
            part_title = re.sub('_哔哩哔哩_bilibili', '', part_title_ori)
            author = soup.find("a", class_="username").text
            # 只取日期部分，去掉时间部分
            date = soup.find("span", class_="pudate-text").text.strip().split(" ")[0]
            return Info(
                type='Video',
                title=', '.join([clear_str(title), clear_str(part_title)]),
                author=clear_str(author),
                source='Bilibili',
                date=clear_str(date),
                url=url,
            )
        except Exception:
            logger.exception(f"Bilibili: `{url}` not found")

        return None

    @classmethod
    def get_info_from_cv(cls, url: str) -> Optional[Info]:
        try:
            soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
            title = soup.find("h1", class_="title").text
            author = soup.find("div", class_="up-name-pannel").text
            # 只取日期部分，去掉时间部分
            date = soup.find("span", class_="publish-text").text.strip().split(" ")[0]
            return Info(
                type='Article',
                title=clear_str(title),
                author=clear_str(author),
                source='Bilibili',
                date=clear_str(date),
                url=url,
            )
        except Exception:
            logger.exception(f"Bilibili: `{url}` not found")

        return None


handlers = (
    BilibiliHandler,
)
