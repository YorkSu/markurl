# -*- coding: utf-8 -*-
import json
from pathlib import Path

from markurl import CONFIG


class Config(object):
    cfg: dict = None

    @staticmethod
    def load_json(file: Path):
        return json.load(file.open('r', encoding='utf-8'))

    @classmethod
    def load_config(cls):
        if cls.cfg is None:
            cls.cfg = cls.load_json(CONFIG)
        return cls.cfg
