from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent
BASE = '/RecLora-rectest/'
ICON = BASE + 'logos/RecLora-rectest/RecLora%20icon.png'
THEME = BASE + 'reclora-theme.css'
REPLACEMENTS = (
    ('/rectest/', '/RecLora-rectest/'), ('rectest', 'reclora'),
    ('recroom.network', 'reclora.network'), ('DreamRec', 'RecLora'),
    ('dreamrec', 'reclora'), ('Dream Rec', 'RecLora'),
    ('Rec Room', 'RecLora'), ('rec room', 'reclora'),
    ('RecRoom', 'RecLora'), ('recroom', 'reclora'),
    ('Studio 87', 'Studio Lora'), ('Studio87', 'StudioLora'),
    ('#FF6727', '#6f3f85'), ('#FF5C00', '#9c5bb2'),
)

def add_brand_shell(text: str) -> str:
    if 'data-reclora-brand' in text:
        return text
    marker = '<body>'
    if marker not in text:
        return text
    brand = (
        f'<div data-reclora-brand class="reclora-brand" role="banner">'
        f'<a href="{BASE}" aria-label="RecLora home">'
        f'<img src="{ICON}" alt="RecLora icon" width="42" height="42">'
        f'<span>RecLora</span></a></div>'
    )
    return text.replace(marker, marker + brand, 1)

def process_html(path: Path) -> None:
    text = path.read_text(encoding='utf-8', errors='ignore')
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = re.sub(r'(content=["\'])https://cdn\.reclora\.network/static/logos/[^"\']+', r'\1' + ICON, text)
    text = re.sub(r'(content=["\'])/logo\.png', r'\1' + ICON, text)
    text = text.replace('dreamrec-links', 'reclora-links').replace('dreamrec-theme.css', 'reclora-theme.css')
    text = text.replace('data-dreamrec-brand', 'data-reclora-brand').replace('dreamrec-brand', 'reclora-brand')
    text = text.replace('DreamRec', 'RecLora')
    text = add_brand_shell(text)
    if text != original:
        path.write_text(text, encoding='utf-8')

def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == 'index.html': return BASE
    if rel.endswith('/index.html'): return BASE + rel[:-len('index.html')]
    return BASE + rel

def make_link_directory() -> None:
    pages = sorted(p for p in ROOT.rglob('*.html') if '.git' not in p.parts and p.name not in {'reclora-links.html'})
    entries = '\n'.join(f'<li><a href="{escape(route_for(p))}">{escape(route_for(p).removeprefix(BASE).strip('/') or "home")}</a></li>' for p in pages)
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RecLora Links</title><link rel="icon" href="{BASE}favicon.ico"><link rel="stylesheet" href="{THEME}"><style>body{{margin:0;font-family:system-ui,sans-serif;background:#170d26;color:#fff9ef}}.reclora-directory{{max-width:1100px;margin:0 auto;padding:1rem 1rem 4rem}}.reclora-directory h1{{margin-top:2rem;color:#f5b041}}.reclora-directory a{{color:#f5b041}}</style></head><body><div class="reclora-brand" data-reclora-brand role="banner"><a href="{BASE}"><img src="{ICON}" alt="RecLora icon" width="42" height="42"><span>RecLora</span></a></div><main class="reclora-directory"><h1>RecLora links</h1><p>{len(pages)} locally mirrored HTML pages and directory routes.</p><ul>{entries}</ul></main></body></html>\n'''
    (ROOT / 'reclora-links.html').write_text(doc, encoding='utf-8')
    (ROOT / 'reclora-links').mkdir(exist_ok=True)
    (ROOT / 'reclora-links' / 'index.html').write_text(doc.replace('href="/RecLora-rectest/reclora-links.html"', 'href="/RecLora-rectest/reclora-links/"'), encoding='utf-8')

for html in ROOT.rglob('*.html'):
    if '.git' not in html.parts and html.name not in {'reclora-links.html'}:
        process_html(html)
make_link_directory()
print(f'Processed {sum(1 for p in ROOT.rglob("*.html"))} HTML files.')
