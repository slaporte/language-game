"""
A utiliscript to process data pulled from List of Wikipedias:

http://en.wikipedia.org/wiki/List_of_wikipedias

I just ran the following jQuery barf in a Chrome console:


var x = $('table.sortable tbody tr:has(td)');
var y = [];
for(var i=0; i<x.length; ++i) {
cur_list = [$(x[i]).find('td:nth-child(2)').text(),
            $(x[i]).find('td:nth-child(2) a').attr('title'),
            $(x[i]).find('td:nth-child(4)').text(),
            $(x[i]).find('td:nth-child(5)').text(),
            $(x[i]).find('td:nth-child(10)').text(), $(x[i]).find('td:nth-child(12)').text()]
if(cur_list[2]) { y.push(cur_list); }
}
JSON.stringify(y);

which results in a list of lists like this:

[u'English', u'w:English language', u'en', u'4,234,378', u'129,657', u'763']
"""

import os
import sys
import json
import re
from pyquery import PyQuery
from wapiti import WapitiClient

wikis_json_filename = sys.argv[1]
wikis_json = open(wikis_json_filename, 'rb').read()
wikis_list = json.loads(wikis_json)
wc = WapitiClient('languagegame@hatnote.com')
RE_INTRO = re.compile(r'(?P<intro>.*?\.)\s*([A-Z\[\n]{1}|\Z)')
RE_FN = re.compile(r'\[[0-9]{1,2}\]')


def parse_count(count_text):
    try:
        return int(count_text.replace(',', '').strip())
    except AttributeError:
        raise


def get_desc(article_name):
    lang_article = wc.web_request_operation('http://en.wikipedia.org/wiki/' + article_name)
    pq = PyQuery(lang_article[0])
    intro_paragraphs = pq('#toc').prevAll('p')
    if not intro_paragraphs:
        intro_paragraphs = pq('#toc').parent().prevAll('p')
    if not intro_paragraphs:
        intro_paragraphs = pq('div#content p')
    if not intro_paragraphs:
        return None
    lang_article_intro = ''.join(intro_paragraphs[0].itertext())
    # remove footnotes
    m = RE_INTRO.match(lang_article_intro)
    if m:
        lang_intro = m.group('intro')
        lang_intro = re.sub(RE_FN, '', lang_intro)
    else:
        return None
    return lang_intro


processed_list = []

for winfo in wikis_list:
    name, article_name, langcode, num_articles, num_active_users, depth = winfo
    if article_name.startswith('w:'):
        article_name = article_name[2:]
    desc = get_desc(article_name)
    if not desc:
        import pdb; pdb.set_trace()
    print '\n * ' + repr(desc)
    num_articles = parse_count(num_articles)
    num_active_users = parse_count(num_active_users)
    depth = depth.replace('-', '').strip()
    depth = depth and int(depth) or 0
    processed_list.append([name, article_name, langcode,
                           num_articles, num_active_users, depth, desc])

assert len(processed_list) == len(wikis_list)
print processed_list[0]
print processed_list[-1]

out_dir = os.path.dirname(os.path.abspath(wikis_json_filename))
out_path = os.path.join(out_dir, 'processed_wikis.json')

with open(out_path, 'wb') as f:
    f.write(json.dumps(processed_list, indent=2))
