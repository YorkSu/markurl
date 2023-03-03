"""
Main
"""


import re
from typing import Callable
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from markurl.arxiv import get_arxiv_info
from markurl.util import info_to_markdown


def get_adapter(url: str) -> Callable:
    # arXiv
    if re.match('.*arxiv.org.*', url) is not None:
        return get_arxiv_info
    
    raise ValueError(f'No Adapter for `{url}`')


parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'url',
    type=str,
    help="the url of resource"
)


def main():
    args = parser.parse_args()
    adapter = get_adapter(args.url)
    info = adapter(args.url)
    markdown = info_to_markdown(info)
    print(markdown)


if __name__ == '__main__':
    main()
