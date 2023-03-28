# -*- coding: utf-8 -*-
"""
Video Handlers

Including BilibiliHandler, YouTubeHandler.

- BilibiliHandler match BVID, bilibili (short) url
- YouTubeHandler match YouTube (short) url

"""
import logging
import re
from typing import Optional

from bs4 import BeautifulSoup
from pytube import YouTube

from markurl.handler.model import Info, Handler
from markurl.util import SESS, PROXIES, clear_str

logger = logging.getLogger('markurl')


class BilibiliHandler(Handler):
    base_url = 'https://www.bilibili.com/video/{bvid}'
    b_pattern = r'((?:https?://)?(?:www\.)?(?:bilibili\.com/video/BV\S{10}|b23\.tv/\S{7}))'
    part_url = 'https://www.bilibili.com/video/{bvid}?p={part}'
    p_pattern = r'(?:https?://)?(?:www\.)?(?:bilibili\.com/video/)(BV\S{10})\?p=(\d+)'

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        # 分P视频
        search = re.findall(cls.p_pattern, url)
        if len(search):
            return cls.get_info_from_part(*search[0])

        # BV号、普通链接、短链接
        _url = cls.get_url(url)
        if _url:
            return cls.get_info(_url)

        return None

    @classmethod
    def get_url(cls, url: str) -> str:
        # BVID
        if re.match(r'BV\S{10}', url) is not None:
            return cls.base_url.format(bvid=url)

        # Extract url from string
        search = re.findall(cls.b_pattern, url)
        return search[0] if len(search) else ''

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


class YouTubeHandler(Handler):
    base_url = 'https://www.youtube.com/watch?v={}'
    y2b_pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([-\w]+)"

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        video = cls.get_url(url)
        if video:
            return cls.get_info(video)

        return None

    @classmethod
    def get_url(cls, url: str) -> str:
        search = re.findall(cls.y2b_pattern, url)
        return search[0] if len(search) else ''

    @classmethod
    def get_info(cls, video: str) -> Optional[Info]:
        try:
            url = cls.base_url.format(video)
            yt = YouTube(url, proxies=PROXIES)
            return Info(
                type='Video',
                title=yt.title,
                author=yt.author,
                source='YouTube',
                date=yt.publish_date.strftime("%Y-%m-%d"),
                url=url,
            )
        except Exception:
            logger.exception(f"YouTube: `{url}` not found")

        return None


handlers = (
    BilibiliHandler,
    YouTubeHandler,
)
