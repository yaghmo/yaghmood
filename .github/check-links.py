from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src") and value:
                url = urlsplit(value)
                if not url.scheme and not url.netloc and url.path:
                    self.paths.append(unquote(url.path))


for page in Path('.').rglob('*.html'):
    parser = Links()
    parser.feed(page.read_text(encoding='utf-8'))
    for link in parser.paths:
        target = page.parent / link
        if target.is_dir():
            target /= 'index.html'
        if not target.is_file():
            raise SystemExit(f'{page}: missing {link}')
print('Local links OK')
