
import feedparser
from bs4 import BeautifulSoup
import os.path

feedparser.PREFERRED_XML_PARSERS.remove('drv_libxml2')
#class RedditRSS(HandlerBase):


module_defs = {'name': 'redditrss',
               'type': 'generator',
               'type': 'final',
               'downloader': 'url',
               'downloader': 'special'}

# libxml2 apparently isn't working with python 3
class Handler:

    name = 'redditrss'
    type = 'generator'

    domain = '^.*reddit.com$'
    path = '^\/r/.*\.rss$'
    
    downloader = 'default'
    priority = 0

    def __init__(self, properties = None):
        self.properties = properties
    
    def get(self, f):

        count = 40
        #feed = feedparser.parse('http://www.reddit.com/r/pics.rss')
        feed = feedparser.parse(f)
        result = []
        
        for e in feed.entries:
            #el = ()
            url = BeautifulSoup(e.description).find_all('a')[2]['href']
            ext = os.path.splitext(url)[1]
            if ext not in ['.jpg', '.png', '.gif', '.bmp', '.jpeg']:
                print(url, "is not an image")
                continue
            #el['url'] = url
            #el['caption'] = e.title
            el = (url, e.title)
            result.append(el)
            if count == 1:
                break
            count -= 1
        print(result)
        return result
        #print(len(result))
        #print(result)


