"""
Utils
"""


import requests


HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}
SESS = requests.Session()
SESS.headers = HEADERS


def get_html(url: str) -> str:
    """
    Get HTML content from arxiv URL
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print(f"Error: failed to get HTML content from {url}")
        return ""


def info_to_markdown(info: dict) -> str:
    """
    Output Markdown format: `title, first author, journal, year, URL, citations`
    """
    pre_text = [
        info['title'],
        info['first_author'],
        info['journal'],
        info['year'],
        f"[URL]({info['url']})",
    ]
    if info['citations'] is not None:
        pre_text.append(info['citations'])
    return ", ".join(pre_text)

