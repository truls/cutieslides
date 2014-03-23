

from handler import Handler

def test():
    h = Handler()
    print(h.get("http://www.reddit.com/r/news.rss"))
    print(h.get("http://www.youtube.com/watch?v=gd_4juHPDaM"))
    print(h.get("http://imgur.com/a/upaLC"))
    print(h.get("http://i.imgur.com/AOSJSi3.gif"))

test()


