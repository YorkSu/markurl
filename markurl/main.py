# -*- coding: utf-8 -*-
"""
Main
"""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from markurl.handler import paper
from markurl.handler import video
from markurl.handler.model import HandlerManager

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'url',
    type=str,
    help="the url of resource"
)
hm = HandlerManager()
hm.extend(
    *video.handlers,
    *paper.handlers,
)


def main():
    args = parser.parse_args()
    url = args.url
    info = hm.handle(url)
    if info:
        print(info)
    else:
        print(f'`{url}` Not Found')


if __name__ == '__main__':
    main()
