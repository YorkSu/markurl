import abc
from typing import Optional, Iterable


class Info(object):
    type: str = None
    title: str = None
    author: str = None
    source: str = None
    date: str = None
    url: str = None
    pdf: str = None
    citations: str = None

    pattern = "**{type}:** {title}, {author}, {source}, {date}, [URL]({url}){additional}"

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

    def to_markdown(self):
        additional = []
        if self.pdf is not None:
            additional.append(f", [PDF]({self.pdf})")
        if self.citations is not None:
            additional.append(f", {self.citations}")
        return self.pattern.format(
            type=self.type,
            title=self.title,
            author=self.author,
            source=self.source,
            date=self.date,
            url=self.url,
            additional=''.join(additional) if len(additional) else ''
        )

    def __repr__(self):
        return self.to_markdown()


class Adapter(abc.ABC):
    _next_adapter: 'Adapter' = None

    @classmethod
    @abc.abstractmethod
    def get(cls, url: str) -> Optional[Info]:
        ...

    @classmethod
    def set_next_adapter(cls, adapter: 'Adapter'):
        cls._next_adapter = adapter

    @classmethod
    def get_next_adapter(cls) -> 'Adapter':
        return cls._next_adapter


class AdapterManager(object):
    head: Adapter = None
    rear: Adapter = None

    def append(self, adapter: Adapter):
        if self.head is None:
            self.head = adapter
            self.rear = adapter
        else:
            self.rear.set_next_adapter(adapter)
            self.rear = adapter

    def extend(self, adapters: Iterable[Adapter]):
        for adapter in adapters:
            self.append(adapter)

    def adapt(self, url: str) -> Optional[Info]:
        # Traverse singly linked list queue
        adapter = self.head
        while adapter is not None:
            _result = adapter.get(url)
            if _result is not None:
                return _result

            # Handed over to the next Adapter
            adapter = adapter.get_next_adapter()

        return None
