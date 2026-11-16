"""Site audit: links, brand leaks, SEO metadata, schema, structure."""
import os, re, json, html, sys
from collections import Counter, defaultdict

DIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dist')
files = {}
for root, _, fs in os.walk(DIST):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            rel = '/' + os.path.relpath(p, DIST).replace(os.sep, '/')
            url = rel[:-len('index.html')].rstrip('/') or '/'
            if f == '404.html':
                url = '/404'
            files[url] = open(p, encoding='utf-8').read()

def visible(s):
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'</?(a|strong|em|span|time|small|b|i|code)(\s[^>]*)?>', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(re.sub(r'\s+', ' ', s))

issues = defaultdict(list)
titles, descs = Counter(), Counter()
inbound = Counter()
LEAK = re.compile(r'Stellar|stellarproperty|Mirsad|Cerimovic|\b2007\b|1,422|96%|AppFolio|appfolio|29 associations|—|–|Mockup only|Needed|TODO')
for url, s in files.items():
    if url == '/404':
        continue
    main = re.search(r'<main id="main">(.*?)</main>', s, re.S)
    body = main.group(1) if main else s
    v = visible(body)
    for m in set(LEAK.findall(v)):
        issues['leak'].append(f'{url}: {m!r} :: ' + v[max(0, v.find(m) - 60):v.find(m) + 60])
    t = re.search(r'<title>(.*?)</title>', s).group(1)
    d = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    titles[t] += 1; descs[d] += 1
    if len(html.unescape(t)) > 70: issues['title>70'].append(f'{url} ({len(t)}): {t}')
    if len(html.unescape(t)) < 25: issues['title<25'].append(f'{url}: {t}')
    if not (70 <= len(html.unescape(d)) <= 165): issues['desc length'].append(f'{url} ({len(d)}): {d}')
    h1 = re.findall(r'<h1[\s>]', s)
    if len(h1) != 1: issues['h1 count'].append(f'{url}: {len(h1)}')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j.replace('<\\/', '</'))
        except Exception as e: issues['ldjson'].append(f'{url}: {e}')
    words = len(v.split())
    if words < 250: issues['thin'].append(f'{url}: {words} words')
    if re.search(r'<p>\s*</p>|<h2>\s*</h2>|<h3>\s*</h3>|<li>\s*</li>', body): issues['empty el'].append(url)
    if re.search(r'\s[,.;:](?=\s|$)', v): issues['stray punctuation'].append(url + ' :: ' + re.search(r'.{40}\s[,.;:](?=\s|$).{0,30}', v).group(0) if re.search(r'.{40}\s[,.;:](?=\s|$).{0,30}', v) else url)
    for h in re.findall(r'href="([^"]+)"', s):
        if h.startswith(('http', 'mailto:', 'tel:', '#', 'javascript')):
            continue
        path = h.split('#')[0].split('?')[0].rstrip('/') or '/'
        if path.startswith('/assets/') or path in ('/sitemap.xml', '/rss.xml', '/robots.txt', '/llms.txt', '/llms-full.txt'):
            if not os.path.exists(os.path.join(DIST, path.lstrip('/'))):
                issues['missing asset'].append(f'{url} -> {h}')
            continue
        if path not in files:
            issues['broken link'].append(f'{url} -> {h}')
        else:
            if path != url: inbound[path] += 1
for t, c in titles.items():
    if c > 1: issues['dup title'].append(f'{c}x {t}')
for d, c in descs.items():
    if c > 1: issues['dup desc'].append(f'{c}x {d[:90]}')
for url in files:
    if url not in ('/', '/404') and inbound[url] < 2:
        issues['orphan-ish (<2 inbound)'].append(f'{url}: {inbound[url]}')
for k, v in issues.items():
    uniq = list(dict.fromkeys(v))
    print(f'\n## {k}: {len(uniq)}')
    for x in uniq[:int(sys.argv[1]) if len(sys.argv) > 1 else 12]:
        print('  ', x[:220])
print('\npages:', len(files))
