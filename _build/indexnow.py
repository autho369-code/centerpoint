"""Submit every sitemap URL to IndexNow (Bing, Yandex, Seznam, Naver, etc.)."""
import json, os, re, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
key = open(os.path.join(HERE, 'indexnow.key')).read().strip()
sm = open(os.path.join(os.path.dirname(HERE), 'dist', 'sitemap.xml'), encoding='utf-8').read()
urls = re.findall(r'<loc>([^<]+)</loc>', sm)
body = json.dumps({'host': 'www.centerpointmgmt.com', 'key': key, 'keyLocation': f'https://www.centerpointmgmt.com/{key}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
r = urllib.request.urlopen(req, timeout=30)
print('IndexNow', r.status, len(urls), 'urls')
