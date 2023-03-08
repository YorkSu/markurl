# -*- coding: utf-8 -*-
"""
Main
"""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from markurl.adapter import paper
from markurl.adapter import video
from markurl.adapter.model import AdapterManager

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'url',
    type=str,
    help="the url of resource"
)
am = AdapterManager()
am.extend(
    *video.adapters,
    *paper.adapters,
)


def main():
    args = parser.parse_args()
    url = args.url
    info = am.adapt(url)
    if info:
        print(info)
    else:
        print(f'`{url}` Not Found')


if __name__ == '__main__':
    main()
