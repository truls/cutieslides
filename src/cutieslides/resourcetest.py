
from resource import *
from handler import *
from config import PropertyBag

def test():
    props = PropertyBag({'caption': 'Caption'})
    h = Handler()
    r = UrlResource("http://www.reddit.com/r/pics.rss", h, properties = props)
    print("Got this list:", r.get_children())

test()

