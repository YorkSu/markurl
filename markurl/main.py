# -*- coding: utf-8 -*-
"""
Main
"""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from markurl.core import default_hm

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'url',
    type=str,
    help="the url of resource"
)


def main():
    args = parser.parse_args()
    url = args.url
    info = default_hm.handle(url)
    if info:
        print(info)
    else:
        print(f'`{url}` Not Found')


if __name__ == '__main__':
    main()
