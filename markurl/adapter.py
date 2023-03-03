import re
import logging
from typing import Callable

from markurl.arxiv import ArxivAdapter
from markurl.crossref import CrossrefAdapter


logger = logging.getLogger('markurl')


def title_adapter(url: str) -> dict:
    # try arXiv Adapter
    infos = ArxivAdapter.get_info_by_title(url)
    if infos is not None:
        return infos
    
    # try Crossref Adapter
    infos = CrossrefAdapter.get_info_by_title(url)
    if infos is not None:
        return infos
    
    # error
    return {}


def get_adapter(url: str) -> Callable:
    # arXiv
    if re.match('.*arxiv.org.*', url) is not None:
        logger.info('arXiv Adapter, url')
        return ArxivAdapter.get_info_by_url
    if re.match('\d{4}\.\d{5}', url) is not None:
        logger.info('arXiv Adapter, id')
        return ArxivAdapter.get_info_by_id
    
    # Crossref
    if re.match('.*doi.org.*', url) is not None:
        logger.info('Crossref Adapter, url')
        return CrossrefAdapter.get_info_by_url
    if re.match('10[.][0-9]{4,}(?:[.][0-9]+)*\/[^\s]+', url) is not None:
        logger.info('Crossref Adapter, id')
        return CrossrefAdapter.get_info_by_id
    
    # title, as default
    logger.info('Title Adapter')
    return title_adapter
    
    # raise ValueError(f'No Adapter for `{url}`')

