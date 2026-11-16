"""Convert a built HTML page into a clean Markdown twin for AI agents."""
import html
import re


def _link(m, site):
    label = re.sub(r'<[^>]+>', ' ', m.group(2))
    label = re.sub(r'\s+', ' ', label).strip()
    href = m.group(1)
    if not href.startswith(('http', 'mailto:', 'tel:')):
        href = site + href
    return f'[{label}]({href})' if label else ''


def to_md(doc, site, name, phone, email):
    m = re.search(r'<main id="main">(.*?)</main>', doc, re.S)
    h = m.group(1) if m else ''
    title = html.unescape(re.search(r'<title>(.*?)</title>', doc).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', doc).group(1))
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', doc)
    h = re.sub(r'<(script|style|svg|form|nav)[^>]*>.*?</\1>', '', h, flags=re.S)
    h = re.sub(r'<i class="[^"]*"></i>', '', h)
    h = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', lambda x: _link(x, site), h, flags=re.S)
    h = re.sub(r'<h1[^>]*>(.*?)</h1>', lambda x: '\n# ' + x.group(1) + '\n', h, flags=re.S)
    h = re.sub(r'<h2[^>]*>(.*?)</h2>', lambda x: '\n## ' + x.group(1) + '\n', h, flags=re.S)
    h = re.sub(r'<(h3|h4|summary)[^>]*>(.*?)</\1>', lambda x: '\n### ' + x.group(2) + '\n', h, flags=re.S)
    h = re.sub(r'<li[^>]*>', '\n- ', h)
    h = re.sub(r'<(strong|b)>(.*?)</\1>', r'**\2**', h, flags=re.S)
    h = re.sub(r'</(p|div|section|ul|ol|tr|details|article|header|aside)>', '\n\n', h)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = html.unescape(h)
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in h.split('\n')]
    h = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()
    url = canon.group(1) if canon else site
    front = f'---\ntitle: {title}\ndescription: {desc}\nurl: {url}\npublisher: {name}\ncontact: {phone}, {email}\n---\n\n'
    return front + h + '\n'
