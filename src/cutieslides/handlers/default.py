
"""
Default handler that matches all URLs ending in a known extension
"""

class Handler(object):

    name = "default"
    type = "final"
    domain = "^.*$"
    path = "^.*\.(jpg|jpeg|gif|png|webm|avi|mp4|flv)$"
    downloader = "default"
    
    priority = 999999

    def __init__(self, properties = None):
        self.properties = properties

    def get(self, f):
        return (f, "")
        #return (f, properties.caption)

    
