# -*- coding: utf-8 -*-
from markurl.handler import bilibili
from markurl.handler import douban
from markurl.handler import paper
from markurl.handler import video
from markurl.handler import webpage
from markurl.handler import wiki
from markurl.handler import zhihu
from markurl.handler import git
from markurl.handler import blog
from markurl.handler.model import HandlerManager

default_hm = HandlerManager()
default_hm.extend(
    *bilibili.handlers,
    *zhihu.handlers,
    *video.handlers,
    *wiki.handlers,
    *douban.handlers,
    *paper.handlers,
    *git.handlers,
    *blog.handlers,
    # default handler
    *webpage.handlers,
)


def handle(hm: HandlerManager, url: str):
    info = hm.handle(url)
    return str(info) or f'`{url}` Not Found'
