import re
from typing import List
from bs4 import PageElement
from crawlutils.num_utils import defaultIfNumber


def get_td(td_list: List[PageElement], *text_in) -> PageElement:
    """
    해당 keyword 를 포함하는 td 를 찾아서 반환한다.
    :param td_list:
    :param text_in:
    :return:
    """
    for td in td_list:
        for text in text_in:
            if text in td.text.replace(" ", ""):
                return td
    return "-"

def get_td_regex(td_list: List[PageElement], regex) -> PageElement:
    """
    해당 keyword 를 포함하는 td 를 찾아서 반환한다.
    :param td_list:
    :param text_in:
    :return:
    """
    compiled_regex = re.compile(regex)
    for td in td_list:
        if compiled_regex.search(td.text.replace(" ", "")):
            return td
    return None


def get_td_text(td_list: List[PageElement], *text_in) -> str:
    """
    해당 td 를 찾아서 그 다음 td 의 text 를 가져온다.
    :param td_list:
    :param text_in:
    :return:
    """
    r = get_td(td_list, *text_in)
    return r.findNext('td').text.strip() if r != "-" else r


def get_td_text_regex(td_list: List[PageElement], regex) -> str:
    """
    해당 td 를 찾아서 그 다음 td 의 text 를 가져온다.
    :param td_list:
    :param text_in:
    :return:
    """
    r = get_td_regex(td_list, regex)
    return r.findNext('td').text.strip() if r is not None else r

def get_td_text_after(td_anchor: PageElement, limit=5, *keyword) -> str:
    """
    :param td_anchor: 기준이 되는 td
    :param limit: anchor 부모 tr 로 부터 몇개의 tr 을 가져올 것인지
    :param keyword: 찾으려는 키워드, 가변키워드, 우선순위가 높은 키워드 부터
    :return:
    """
    if td_anchor is None:
        return None
    trs: List[PageElement] = td_anchor.parent.findNextSiblings('tr')

    if len(trs) < 1:
        return None

    trs = trs[:limit]
    tds = []
    for tr in trs:
        tds.extend(tr.findAll('td'))

    return get_td_text(tds, *keyword)


def find_tr_has_text(text, trlist) -> PageElement:
    target_tr = None
    for tr in trlist:
        if text in tr.text.replace(' ', ''):
            target_tr = tr
            break
    return target_tr


def find_table_has_text(table_list: List[PageElement], *keywords) -> PageElement:
    for table in table_list:
        for keyword in keywords:
            if keyword in table.text.replace(' ', ''):
                return table
    return None


def defaultNumberInTR(text, tr3, unit_multiplier, default="-"):
    np_tr = find_tr_has_text(text, tr3)
    np = defaultIfNumber(np_tr.findAll('td')[1].text, unit_multiplier, default=default)
    return np