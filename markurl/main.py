"""
Main
"""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from markurl.util import info_to_markdown
from markurl.adapter import get_adapter


parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'url',
    type=str,
    help="the url of resource"
)


def main():
    args = parser.parse_args()
    url = args.url
    adapter = get_adapter(url)
    info = adapter(url)
    if info:
        markdown = info_to_markdown(info)
        print(markdown)
    else:
        print(f'{url} Not Found')


if __name__ == '__main__':
    main()
