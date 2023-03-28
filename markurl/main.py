# -*- coding: utf-8 -*-
"""
Main
"""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from markurl.core import default_hm
from markurl.handler.paper import TitleHandler

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'url',
    type=str,
    help="the url of resource"
)
parser.add_argument(
    '-t', '--title_only',
    action='store_true',
    help="search the given title from arxiv and crossref"
)


def main():
    args = parser.parse_args()
    url = args.url

    if args.title_only:
        info = TitleHandler.get(url)
    else:
        info = default_hm.handle(url)

    if info:
        print(info)
    else:
        print(f'`{url}` Not Found')


if __name__ == '__main__':
    main()
