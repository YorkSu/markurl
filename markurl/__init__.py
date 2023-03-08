# -*- coding: utf-8 -*-
""""MarkURL, a tool for generating formatted Markdown from URLs"""
from pathlib import Path


PROJECT = HERE = Path(__file__).parent
ROOT = HERE.parent
CONFIG = ROOT / 'config.json'
MARKFILE = ROOT / 'markfile.md'
OUTPUTFILE = ROOT / 'output.md'
