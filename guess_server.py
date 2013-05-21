# -*- coding: utf-8 -*-

import os
from os.path import join as pjoin
import random

from pyquery import PyQuery

import wapiti
from clastic import Application
from clastic.render.mako_templates import MakoRenderFactory


_CURDIR = os.path.abspath(os.path.dirname(__file__))
_TEMPLATE_PATH = pjoin(_CURDIR, 'templates')
_STATIC_PATH = pjoin(_CURDIR, 'templates', 'assets')
_LANG_DICT = {
    "English": "en",
    "German": "de",
    "Dutch": "nl",
    "French": "fr",
    "Italian": "it",
    "Spanish": "es",
    "Russian": "ru",
    "Swedish": "sv",
    "Polish": "pl",
    "Japanese": "ja",
    "Portuguese": "pt",
    "Chinese": "zh",
    "Vietnamese": "vi",
    "Ukrainian": "uk",
    "Catalan": "ca",
    "Waray-Waray":    "war",
    "Cebuano": "ceb",
    "Finnish": "fi",
    "Persian": "fa",
    "Czech": "cs",
    "Hungarian": "hu",
    "Korean": "ko",
    "Arabic": "ar",
    "Romanian": "ro",
    "Malay": "ms",
    "Turkish": "tr",
    "Indonesian": "id",
    "Kazakh": "kk",
    "Serbian": "sr",
    "Slovak": "sk",
    "Esperanto": "eo",
    "Danish": "da",
    "Lithuanian": "lt",
    "Basque": "eu",
    "Bulgarian": "bg",
    "Hebrew": "he",
    "Croatian": "hr",
    "Slovenian": "sl",
    "Uzbek": "uz",
    "Volap\u00fck":    "vo",
    "Estonian": "et",
    "Hindi": "hi",
    "Norwegian (Nynorsk)":    "nn",
    "Galician": "gl",
    "Simple English ":    "simple",
    "Azerbaijani": "az",
    "Latin": "la",
    "Greek": "el",
    "Serbo- Croatian":    "sh",
    "Thai": "th",
    "Georgian": "ka",
    "Macedonian": "mk",
    "Occitan": "oc",
    "Newar/Nepal Bhasa":    "new",
    "Piedmontese": "pms",
    "Tagalog": "tl",
    "Belarusian": "be",
    "Tamil": "ta",
    "Haitian": "ht",
    "Telugu": "te",
    "Belarusian (Tara\u0161kievica)":    "be-x-old",
    "Welsh": "cy",
    "Latvian": "lv",
    "Bosnian": "bs",
    "Breton": "br",
    "Albanian": "sq",
    "Armenian": "hy",
    "Malagasy": "mg",
    "Tatar": "tt",
    "Javanese": "jv",
    "Marathi": "mr",
    "Luxembourgish": "lb",
    "Icelandic": "is",
    "Burmese": "my",
    "Yoruba": "yo",
    "Malayalam": "ml",
    "Bashkir": "ba",
    "Aragonese": "an",
    "Lombard": "lmo",
    "Afrikaans": "af",
    "West Frisian ":    "fy",
    "Western Panjabi ":    "pnb",
    "Bengali": "bn",
    "Swahili": "sw",
    "Bishnupriya Manipuri ":    "bpy",
    "Ido": "io",
    "Kirghiz": "ky",
    "Urdu": "ur",
    "Nepali": "ne",
    "Sicilian": "scn",
    "Cantonese": "zh-yue",
    "Gujarati": "gu",
    "Low Saxon ":    "nds",
    "Irish": "ga",
    "Kurdish": "ku",
    "Asturian": "ast",
    "Quechua": "qu",
    "Sundanese": "su",
    "Chuvash": "cv",
    "Scots": "sco",
    "Alemannic": "als",
    "Interlingua": "ia",
    "Neapolitan": "nap",
    "Buginese": "bug",
    "Samogitian": "bat-smg",
    "Kannada": "kn",
    "Banyumasan": "map-bms",
    "Walloon": "wa",
    "Amharic": "am",
    "Sorani": "ckb",
    "Scottish Gaelic ":    "gd",
    "Fiji Hindi ":    "hif",
    "Min Nan ":    "zh-min-nan",
    "Tajik": "tg",
    "Egyptian Arabic ":    "arz",
    "Mazandarani": "mzn",
    "Yiddish": "yi",
    "Venetian": "vec",
    "Mongolian": "mn",
    "Nahuatl": "nah",
    "Tarantino": "roa-tara",
    "Sakha": "sah",
    "Sanskrit": "sa",
    "Ossetian": "os",
    "Kapampangan": "pam",
    "Upper Sorbian ":    "hsb",
    "Sinhalese": "si",
    "Northern Sami ":    "se",
    "Bavarian": "bar",
    "Limburgish": "li",
    "Maori": "mi",
    "Corsican": "co",
    "Gan": "gan",
    "Faroese": "fo",
    "Ilokano": "ilo",
    "Tibetan": "bo",
    "Punjabi": "pa",
    "Gilaki": "glk",
    "Rusyn": "rue",
    "Central Bicolano": "bcl",
    "V\ u00f5ro":    "fiu-vro",
    "Hill Mari ":    "mrj",
    "Dutch Low Saxon":    "nds-nl",
    "Turkmen": "tk",
    "Pashto": "ps",
    "West Flemish ":    "vls",
    "Mingrelian": "xmf",
    "Manx": "gv",
    "Zazaki": "diq",
    "Oriya": "or",
    "Komi": "kv",
    "Pangasinan": "pag",
    "Zeelandic": "zea",
    "Khmer": "km",
    "Divehi": "dv",
    "Norman": "nrm",
    "Meadow Mari ":    "mhr",
    "Romansh": "rm",
    "Komi- Permyak":    "koi",
    "Udmurt": "udm",
    "Kashubian": "csb",
    "North Frisian ":    "frr",
    "Vepsian": "vep",
    "Ladino": "lad",
    "Ligurian": "lij",
    "Wu": "wuu",
    "Friulian": "fur",
    "Classical Chinese ":    "zh-classical",
    "Uyghur": "ug",
    "Sardinian": "sc",
    "Saterland Frisian ":    "stq",
    "Aymara": "ay",
    "Maltese": "mt",
    "Pali": "pi",
    "Somali": "so",
    "Bihari": "bh",
    "Ripuarian": "ksh",
    "Novial": "nov",
    "Anglo- Saxon":    "ang",
    "Hakka": "hak",
    "Cornish": "kw",
    "Navajo": "nv",
    "Picard": "pcd",
    "Guarani": "gn",
    "Extremaduran": "ext",
    "Assamese": "as",
    "Silesian": "szl",
    "Gagauz": "gag",
    "Emilian- Romagnol":    "eml",
    "Interlingue": "ie",
    "Lingala": "ln",
    "Acehnese": "ace",
    "Chechen": "ce",
    "Karachay- Balkar":    "krc",
    "Palatinate German ":    "pfl",
    "Kalmyk": "xal",
    "Hawaiian": "haw",
    "Pennsylvania German ":    "pdc",
    "Kinyarwanda": "rw",
    "Crimean Tatar ":    "crh",
    "Tongan": "to",
    "Lower Sorbian ":    "dsb",
    "Greenlandic": "kl",
    "Aramaic": "arc",
    "Erzya": "myv",
    "Kabyle": "kab",
    "Lezgian": "lez",
    "Banjar": "bjn",
    "Shona": "sn",
    "Papiamentu": "pap",
    "Tok Pisin ":    "tpi",
    "Lak": "lbe",
    "Wolof": "wo",
    "Lojban": "jbo",
    "Moksha": "mdf",
    "Zamboanga Chavacano ":    "cbk-zam",
    "Avar": "av",
    "Kabardian Circassian ":    "kbd",
    "Sranan": "srn",
    "Mirandese": "mwl",
    "Tahitian": "ty",
    "Lao": "lo",
    "Abkhazian": "ab",
    "Tetum": "tet",
    "Latgalian": "ltg",
    "Kongo": "kg",
    "Nauruan": "na",
    "Igbo": "ig",
    "Buryat (Russia)":    "bxr",
    "Northern Sotho ":    "nso",
    "Zhuang": "za",
    "Karakalpak": "kaa",
    "Zulu": "zu",
    "Cheyenne": "chy",
    "Romani": "rmy",
    "Old Church Slavonic":    "cu",
    "Aromanian": "roa-rup",
    "Tswana": "tn",
    "Cherokee": "chr",
    "Bislama": "bi",
    "Min Dong ":    "cdo",
    "Gothic": "got",
    "Samoan": "sm",
    "Moldovan": "mo",
    "Bambara": "bm",
    "Inuktitut": "iu",
    "Norfolk": "pih",
    "Pontic": "pnt",
    "Sindhi": "sd",
    "Swati": "ss",
    "Kikuyu": "ki",
    "Ewe": "ee",
    "Hausa": "ha",
    "Oromo": "om",
    "Fijian": "fj",
    "Tigrinya": "ti",
    "Tsonga": "ts",
    "Kashmiri": "ks",
    "Venda": "ve",
    "Sango": "sg",
    "Kirundi": "rn",
    "Sesotho": "st",
    "Dzongkha": "dz",
    "Akan": "ak",
    "Cree": "cr",
    "Tumbuka": "tum",
    "Luganda": "lg",
    "Inupiak": "ik",
    "Fula": "ff",
    "Chichewa": "ny",
    "Twi": "tw",
    "Chamorro": "ch",
    "Xhosa": "xh",
    "Ndonga": "ng",
    "Sichuan Yi ":    "ii",
    "Choctaw": "cho",
    "Marshallese": "mh",
    "Afar": "aa",
    "Kuanyama": "kj",
    "Hiri Motu ":    "ho",
    "Muscogee": "mus",
    "Kanuri": "kr",
    "Herero": "hz"}


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
    #lang = 'Spanish'  # a good way to debug
    lang_url = 'http://%s.wikipedia.org/' % (_LANG_DICT[lang],)
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
