

import re
import os

from urllib.parse import urlparse

# Get builtin handlers
#import handlers

class PropertyWrapper(object):

    def __init__(self, name = None, type = None,
                 domain = None, path = None, downloader = None, priority = None):
        # FIXME: Most of these attributes should be required
        self.name = name or "noname"
        self.type = name or "final"
        self.domain = re.compile(domain) or re.compile("")
        self.path = re.compile(path) or re.compile("")
        self.downloader = downloader or "default"
        self.priority = 0 or priority

    def __getattr__(self, attr):
        return getattr(self, attr)
    

class Handler(object):

    def __init__(self, handler_dirs = []):

        self.handler_dirs = ["handlers"] + handler_dirs
        
        self.handlers = []

        for hd in self.handler_dirs:
            fs = os.listdir(hd)
            for f in fs:
                mod = os.path.splitext(f)[0]
                if mod.startswith('__'):
                    continue

                print("Trying to import ", mod)
                
                h = getattr(__import__("handlers." + mod), mod)
                print(dir(h))
                print(h.Handler.name)
                self.handlers.append((h.Handler, PropertyWrapper(name = h.Handler.name,
                                                              type = h.Handler.type,
                                                              domain = h.Handler.domain,
                                                              path = h.Handler.path,
                                                              downloader = h.Handler.downloader,
                                                              priority = h.Handler.priority)))
    def get(self, url):
        o = urlparse(url)

        # Try to find a matching handler
        for k, v in sorted(self.handlers, key=lambda k: k[1].priority):
            print(v.domain, o.netloc, v.path, o.path)
            # FIXME: Handle URLs with port numbers
            if not v.domain.match(o.netloc):
                continue
            print("Matched domain")
            if not v.path.match(o.path):
                continue

            return k
                
