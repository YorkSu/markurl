# -*- coding: utf-8 -*-
"""
Video Handlers

Including YouTubeHandler.

- YouTubeHandler match YouTube (short) url

"""
import logging
import re
from typing import Optional

from pytube import YouTube

from markurl.handler.model import Info, Handler
from markurl.util import PROXIES

logger = logging.getLogger('markurl')


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
    YouTubeHandler,
)
