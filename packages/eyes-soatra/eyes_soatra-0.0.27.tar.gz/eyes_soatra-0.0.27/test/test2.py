#!python3
from eyes_soatra import eyes
import requests
import json
from lxml.html.clean import Cleaner
from lxml import html
from lxml import etree
import re
from translate import Translator
import pandas

a = eyes.view_page(
    url='https://www.town.omachi.lg.jp'
)

print(a)