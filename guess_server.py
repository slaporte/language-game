# -*- coding: utf-8 -*-

import os
from os.path import join as pjoin
import json
import random
from collections import namedtuple

from pyquery import PyQuery

import wapiti
from clastic import Application
from clastic.render.mako_templates import MakoRenderFactory


WikiLangInfo = namedtuple('WikiLangInfo',
                          'name, en_article_name, shortcode, article_count, '
                          'active_user_count, depth')


_CURDIR = os.path.abspath(os.path.dirname(__file__))
_TEMPLATE_PATH = pjoin(_CURDIR, 'templates')
_STATIC_PATH = pjoin(_CURDIR, 'templates', 'assets')


def load_langs():
    """
    File format:
    [[u'English', u'English language', u'en', 4234378, 129657, 763], ...]

    (Language name, English Wikipedia article, shortcode, number of articles,
    number of active users, depth metric)
    """
    ret = {}
    with open(pjoin(_CURDIR, 'wikis.json')) as f:
        wiki_lists = json.loads(f.read())
    for wiki in wiki_lists:
        wli = WikiLangInfo(*wiki)
        ret[wli.name] = wli
    return ret


_LANG_DICT = load_langs()


def get_text(element):
    if hasattr(element, 'text_content'):  # lxml 2
        text = element.text_content()
    else:
        text = u''.join(element.itertext())
    return text


def get_sample(page_text):
    sample = page_text[:500]
    if len(sample) == 500:
        sample = sample.rsplit(None, 1)[0]
        return sample + ' ...'
    return sample


def get_random_page():
    lang = random.choice(_LANG_DICT.keys())
    lang_info = _LANG_DICT[lang]
    #lang = 'Spanish'  # a good way to debug
    lang_url = 'http://%s.wikipedia.org/' % (lang_info.shortcode,)
    lang_api_url = pjoin(lang_url, 'w/api.php')
    wc = wapiti.WapitiClient('languagegame@hatnote.com',
                             api_url=lang_api_url)
    pages = wc.get_random_articles(limit=1)
    page_title = pages[0].title
    page_url = pjoin(lang_url, 'wiki', page_title)
    contents = wc.web_request_operation(page_url)
    return lang, contents, page_title


def language_game(attempt=0):
    choices = []
    correct, contents, title = get_random_page()
    choices.append(correct)
    choices.extend(random.sample(_LANG_DICT.keys(), 4))
    random.shuffle(choices)
    decoded_contents = contents[0].decode('utf-8')
    pq = PyQuery(decoded_contents)
    # Is PyQuery even necessary?
    content_div = pq('div#mw-content-text')
    paragraphs = content_div.find('p')
    try:
        sample_p = paragraphs[0]
    except IndexError:
        # TODO: a much better retry
        return language_game(attempt=attempt + 1)
    page_text = get_text(sample_p)
    sample = get_sample(page_text)
    ret = {
        'correct': correct,
        'choices': choices,
        'sample': sample,
        'title': title
    }
    return ret


def create_game():
    routes = [('/', language_game, 'layout.html')]
    mako_render = MakoRenderFactory(_TEMPLATE_PATH)
    return Application(routes, None, mako_render)


if __name__ == '__main__':
    create_game().serve(static_path=_STATIC_PATH)
