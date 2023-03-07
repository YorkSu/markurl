import re

from bs4 import BeautifulSoup

from dev.old_test.adapter import Adapter
from markurl.util import SESS


class BilibiliAdapter(Adapter):
    base_url = 'https://www.bilibili.com/video/{}'

    @classmethod
    def extract(cls, url: str) -> str:
        # BVID
        if re.match('BV[\S]{10}', url) is not None:
            return cls.base_url.format(url)
        
        # Extract url from string
        search = re.findall(
            r'(https?://(?:www\.bilibili\.com/video/BV\S{10}|b23\.tv/\S{7}))',
            url
        )
        return search[0] if len(search) else ''

    @staticmethod
    def get_info(url: str) -> dict:
        soup = BeautifulSoup(SESS.get(url).text, 'html.parser')
        title = soup.find("h1", class_="tit").text.strip()
        up = soup.find("a", class_="username").text.strip()
        # 只取日期部分，去掉时间部分
        time = soup.find("span", class_="pudate-text").text.strip().split(" ")[0]
        real_url = soup.find("meta", property="og:url")['content']
        return {
            'type': 'Video',
            'title': title,
            'author': up,
            'source': 'Bilibili',
            'year': time,
            'url': real_url,
            'pdf': None,
            'citations': None,
        }

    @classmethod
    def get_info_extract(cls, url: str) -> dict:
        return cls.get_info(cls.extract(url))
