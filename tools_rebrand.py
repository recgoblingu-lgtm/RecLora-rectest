from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent
BASE = "/reclora/"
ICON = BASE + "logos/reclora/RecLora%20icon.png"
THEME = BASE + "reclora-theme.css"

# Site-level copy and metadata only. User-generated titles, room names, and profile names remain untouched.
REPLACEMENTS = (
    ("reclora.network", "RecLora"),
    ("RecLora is the best place to build and play games together.", "RecLora is a community hub for discovering rooms, creators, events, and profiles."),
    ("Purchase subscriptions or tokens for RecLora.", "Explore RecLora subscriptions and community features."),
    ("Rooms in RecLora", "Rooms in RecLora"),
    ("Creator Hub", "RecLora Creator Hub"),
    ("RecLora Shop", "RecLora Shop"),
    ("RecLora", "RecLora"),
    ("#FF6727", "#16b7b0"),
    ("#FF5C00", "#0b7180"),
)


def add_brand_shell(text: str) -> str:
    if "data-reclora-brand" in text:
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
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    # Use the local RecLora mark for site-level Open Graph/Twitter images, not room/profile artwork.
    text = re.sub(r'(content=["\'])https://cdn\.reclora\.network/static/logos/[^"\']+', r'\1' + ICON, text)
    text = re.sub(r'(content=["\'])/logo\.png', r'\1' + ICON, text)
    text = text.replace(f'href="{THEME}"', f'href="{THEME}"')
    text = add_brand_shell(text)
    if text != original:
        path.write_text(text, encoding="utf-8")


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return BASE
    if rel.endswith("/index.html"):
        return BASE + rel[:-len("index.html")]
    return BASE + rel


def make_link_directory() -> None:
    pages = sorted(
        p for p in ROOT.rglob("*.html")
        if ".git" not in p.parts and "tools_rebrand.py" not in p.name
        and p.name not in {"reclora-links.html"}
    )
    entries = []
    for p in pages:
        route = route_for(p)
        label = route.removeprefix(BASE).strip("/") or "home"
        entries.append(f'<li><a href="{escape(route)}">{escape(label)}</a></li>')
    body = "\n".join(entries)
    doc = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RecLora Links</title>
<meta name="description" content="Browse every locally mirrored RecLora HTML route.">
<link rel="icon" href="{BASE}favicon.ico"><link rel="stylesheet" href="{THEME}">
<style>
body{{margin:0;font-family:system-ui,sans-serif;background:#061a2a;color:#e6fbf8}}
.reclora-directory{{max-width:1100px;margin:0 auto;padding:1rem 1rem 4rem}}
.reclora-directory h1{{margin-top:2rem;color:#67eee0}}
.reclora-directory p{{color:#9bc8ca}}
.reclora-directory ul{{columns:3 280px;column-gap:2rem;padding:0;list-style:none}}
.reclora-directory li{{break-inside:avoid;margin:.35rem 0}}
.reclora-directory a{{color:#67eee0;text-decoration:none}}
.reclora-directory a:hover{{text-decoration:underline}}
</style></head><body>
<div class="reclora-brand" data-reclora-brand role="banner"><a href="{BASE}"><img src="{ICON}" alt="RecLora icon" width="42" height="42"><span>RecLora</span></a></div>
<main class="reclora-directory"><h1>RecLora links</h1><p>{len(pages)} locally mirrored HTML pages and directory routes.</p><ul>{body}</ul></main>
</body></html>\n'''
    (ROOT / "reclora-links.html").write_text(doc, encoding="utf-8")
    (ROOT / "reclora-links").mkdir(exist_ok=True)
    (ROOT / "reclora-links" / "index.html").write_text(doc.replace('href="/reclora/reclora-links.html"', 'href="/reclora/reclora-links/"'), encoding="utf-8")


for html in ROOT.rglob("*.html"):
    if ".git" not in html.parts and html.name not in {"reclora-links.html"}:
        process_html(html)
make_link_directory()
print(f"Processed HTML pages and generated link directory from {len(list(ROOT.rglob('*.html')))} files.")
атtributes = None
THOOK = None
