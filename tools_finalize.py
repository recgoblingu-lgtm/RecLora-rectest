from pathlib import Path

ROOT = Path(__file__).resolve().parent
LINK = '/reclora/reclora-links.html'
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts or path.name == 'reclora-links.html':
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'data-reclora-brand' in text and 'reclora-directory-link' not in text:
        text = text.replace('</span></a></div>', f'</span></a><a class="reclora-directory-link" href="{LINK}">All links</a></div>', 1)
        path.write_text(text, encoding='utf-8')
for path in (ROOT / 'reclora-links.html', ROOT / 'reclora-links' / 'index.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'reclora-directory-link' not in text:
        text = text.replace('</span></a></div>', f'</span></a><a class="reclora-directory-link" href="{LINK}">All links</a></div>', 1)
        path.write_text(text, encoding='utf-8')
md = ROOT / 'reclora-links.md'
if md.exists() and 'Complete generated directory' not in md.read_text(encoding='utf-8'):
    extra = '\n## Complete generated directory\n\n- /reclora/reclora-links.html\n- /reclora/reclora-links/\n'
    md.write_text(md.read_text(encoding='utf-8').rstrip() + extra, encoding='utf-8')
txt = ROOT / 'reclora-links.txt'
if txt.exists() and 'reclora-links.html' not in txt.read_text(encoding='utf-8'):
    txt.write_text(txt.read_text(encoding='utf-8').rstrip() + '\n/reclora/reclora-links.html\n/reclora/reclora-links/\n', encoding='utf-8')
print('Finalized RecLora navigation and route manifests.')
