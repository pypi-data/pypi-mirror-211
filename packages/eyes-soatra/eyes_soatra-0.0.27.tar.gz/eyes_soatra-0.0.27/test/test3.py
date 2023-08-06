#!python3
from eyes_soatra import eyes
import json

res = eyes.time_app(
    url = 'https://www.city.tagajo.miyagi.jp:443/fukushi/kenko/fukushi/tyouikin.html'
)
js = json.dumps(
    res,
    ensure_ascii=False,
    indent=4
)

print(js)