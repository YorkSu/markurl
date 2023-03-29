# -*- coding: utf-8 -*-
import abc
from typing import Optional, Type, TypeVar

from markurl.config import Config

cfg = Config.load_config()


class Info(object):
    type: str = None
    title: str = None
    author: str = None
    source: str = None
    date: str = None
    url: str = None
    pdf: str = None
    citations: str = None

    _pattern = "**{type}:** {title}, {author}, {source}, {date}, [URL]({url}){additional}"

    def __init__(self,
                 type: str = None,
                 title: str = None,
                 author: str = None,
                 source: str = None,
                 date: str = None,
                 url: str = None,
                 pdf: str = None,
                 citations: str = None):
        super().__init__()
        self.type = type
        self.title = title
        self.author = author
        self.source = source
        self.date = date
        self.url = url
        self.pdf = pdf
        self.citations = citations

    @property
    def pattern(self):
        return cfg.get('markdown', {}).get('fmt', self._pattern)

    @property
    def pattern_basic(self):
        return cfg.get('markdown', {}).get('fmt_basic', self._pattern)

    def to_markdown(self):
        additional = []
        pattern = self.pattern_basic

        if self.author is not None:
            additional.append(f", {self.author}")
        if self.date is not None:
            additional.append(f", {self.date}")

        if self.pdf is not None:
            additional.append(f", [PDF]({self.pdf})")
        if self.citations is not None:
            additional.append(f", {self.citations}")

        # return self.pattern.format(
        #     type=self.type,
        #     title=self.title,
        #     author=self.author,
        #     source=self.source,
        #     date=self.date,
        #     url=self.url,
        #     additional=''.join(additional) if len(additional) else ''
        # )

        return pattern.format(
            type=self.type,
            title=self.title,
            source=self.source,
            url=self.url,
            additional=''.join(additional) if len(additional) else ''
        )

    def __repr__(self):
        return self.to_markdown()


class Handler(abc.ABC):
    _next_handler: 'Handler' = None

    @classmethod
    @abc.abstractmethod
    def get(cls, url: str) -> Optional[Info]:
        ...

    @classmethod
    def set_next_adapter(cls, handler: 'Handler'):
        cls._next_handler = handler

    @classmethod
    def get_next_adapter(cls) -> 'Handler':
        return cls._next_handler


HandlerSubclass = TypeVar('HandlerSubclass', bound=Type[Handler])


class HandlerManager(object):
    head: HandlerSubclass = None
    rear: HandlerSubclass = None

    def append(self, handler: HandlerSubclass):
        if self.head is None:
            self.head = handler
            self.rear = handler
        else:
            self.rear.set_next_adapter(handler)
            self.rear = handler

    def extend(self, *handlers: HandlerSubclass):
        for handler in handlers:
            self.append(handler)

    def handle(self, url: str) -> Optional[Info]:
        # Traverse singly linked list queue
        handler = self.head
        while handler is not None:
            _result = handler.get(url)
            if _result is not None:
                return _result

            # Handed over to the next Adapter
            handler = handler.get_next_adapter()

        return None
