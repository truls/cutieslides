# -*- coding: utf-8 -*-

import pyinotify
import yaml
import os
import random
from threading import Lock

# FIXME: The inotify modify event appears to be triggered twice. Figure out why this is

# TODO: Add support for the frequency config option

class FileEventHandler(pyinotify.ProcessEvent):
    def __init__(self, parent):
        self.parent = parent
        super(pyinotify.ProcessEvent, self).__init__()

    def process_IN_MODIFY(self, e):
        if e.name == self.parent.config_basename:
            print("Reloading config")
            self.parent.lock.acquire(True)
            self.parent.read_config()
            self.parent.lock.release()
        
#class DictWrapper(object):
#    def __init__(self, d):
#        self.dict = 

class Config(object):
    
    def __init__(self, f):
        self.configfile = f

        self.config_dict = {}
        self.slides = []

        self.reloaded = False
        self.lock = Lock()

        self.read_config()

        # Start threaded inotify to monitor config file for changes
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_MODIFY
        handler = FileEventHandler(self)
        path, self.config_basename = os.path.split(self.configfile)
        wm.add_watch(path, mask, rec=True)
        
        self.notifier = pyinotify.ThreadedNotifier(wm, handler)
        self.notifier.start()
        
    def read_config(self):
        try:
            with open(self.configfile) as fp:
                self.config = yaml.safe_load(fp)
        except yaml.parser.ParserError as e:
            print("Config file parse error " + str(e))
            return
        
        self.slides = sum([[el]*el['frequency'] for el in self.config['slides']], [])
        # Expand filenames:
        self.slides = [self._expand_path(el) for el in self.slides]
        #self.slides = sum([self._expand_directory(el) for el in self.slides if
        #                   el.has_key("directory")], [])
        print(self.slides)
        if self.config['randomize']:
            random.shuffle(self.slides)
        print(self.slides)

        self.reloaded = True
    
    def next(self):
        while True:
            for s in self.slides:
                self.lock.acquire(True)
                if self.reloaded:
                    self.reloaded = False
                    self.lock.release()
                    break
                yield s
                self.lock.release()
                
    def _expand_path(self, el):
        el["file"] = os.path.join(self.config['basepath'], el["file"])
        return el

    def _expand_directory(self, el):
        pass
    
    def end(self):
        self.notifier.stop()


