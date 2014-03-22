
import feedparser
from bs4 import BeautifulSoup
import os.path

count = 10
feed = feedparser.parse("http://www.reddit.com/r/pics.rss")
result = []

for e in feed.entries:
    el = {}
    url = BeautifulSoup(e.description).find_all('a')[2]['href']
    ext = os.path.splitext(url)[1]
    if ext not in ['.jpg', '.png', '.gif', '.bmp', '.jpeg']:
        print(url, "is not an image")
        continue
    el['url'] = url
    el['caption'] = e.title
    result.append(el)
    if count == 1:
        break
    count -= 1

print(len(result))
print(result)

