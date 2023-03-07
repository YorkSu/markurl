"""
Video Adapters

Including BilibiliAdapter, CrossrefAdapter and TitleAdapter.

- BilibiliAdapter match BVID, bilibili (short) url

"""
import logging
import re
from typing import Optional

from bs4 import BeautifulSoup
from pytube import YouTube

from markurl.model import Info, Adapter
from markurl.util import SESS, PROXIES, clear_str

logger = logging.getLogger('markurl')


class BilibiliAdapter(Adapter):
    base_url = 'https://www.bilibili.com/video/{}'

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        _url = cls.get_url(url)
        if _url:
            return cls.get_info(_url)

        return None

    @classmethod
    def get_url(cls, url: str) -> str:
        # BVID
        if re.match(r'BV\S{10}', url) is not None:
            return cls.base_url.format(url)

        # Extract url from string
        search = re.findall(
            r'(https?://(?:www\.bilibili\.com/video/BV\S{10}|b23\.tv/\S{7}))',
            url
        )
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


class YouTubeAdapter(Adapter):
    base_url = 'https://www.youtube.com/watch?v={}'

    @classmethod
    def get(cls, url: str) -> Optional[Info]:
        _url = cls.get_url(url)
        if _url:
            return cls.get_info(_url)

        return None

    @classmethod
    def get_url(cls, url: str) -> str:
        youtube_regex = r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([-\w]+)"
        matches = re.findall(youtube_regex, url)
        if len(matches):
            return cls.base_url.format(matches[0])

        return ''

    @classmethod
    def get_info(cls, url: str) -> Optional[Info]:
        try:
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


adapters = (
    BilibiliAdapter,
    YouTubeAdapter,
)
