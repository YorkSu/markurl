# -*- coding: utf-8 -*-
from markurl.handler import paper
from markurl.handler import video
from markurl.handler.model import HandlerManager

default_hm = HandlerManager()
default_hm.extend(
    *video.handlers,
    *paper.handlers,
)

video_hm = HandlerManager()
video_hm.extend(
    *video.handlers
)

paper_hm = HandlerManager()
paper_hm.extend(
    *paper.handlers
)


def handle(hm: HandlerManager, url: str):
    info = hm.handle(url)
    return str(info) or f'`{url}` Not Found'
