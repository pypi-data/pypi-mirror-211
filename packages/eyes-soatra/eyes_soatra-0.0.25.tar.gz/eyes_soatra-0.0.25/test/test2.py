#!python3
from eyes_soatra import eyes
import requests
import json
from lxml.html.clean import Cleaner
from lxml import html
from lxml import etree
import re
from translate import Translator

a = eyes.view_page(
    url='https://www.hokkaido-esashi.jp/modules/lifeinfo/content0937.html',
    # show_detail=True,
)
js = json.dumps(a, ensure_ascii=False, indent=4)
print(js)
