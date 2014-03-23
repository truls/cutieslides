# -*- coding: utf-8 -*-

import pyinotify
import yaml
import os
import random
from copy import deepcopy
from threading import Lock
from PyQt4.QtCore import QObject, pyqtSignal
from resource import FilesystemResource, UrlResource

class PropertyBag(object):
    
    def __init__(self, initval = {}):
        # Avoid triggering __setattr__
        self.__dict__["_val"] = initval
        print(self._val)

    def update(self, other):
        self._val.update(other)

    def clone(self, **kwargs):
        new = deepcopy(self._val)
        if len(kwargs) > 0:
            for k, v in kwargs.items():
                new[k] = v
        
        return PropertyBag(new)

    def __getattr__(self, k):
        if not k in self._val:
            raise AttributeError
        return self._val[k]

    def __setattr__(self, k, v):
        self._val[k] = v

# TODO:
# Add inotify listeners for "directory" entries so that files added
# to a directory will show up in slides automatically

# FIXME: The inotify modify event appears to be triggered twice. Figure out why this is

class FileEventHandler(pyinotify.ProcessEvent):
    def __init__(self, parent):
        self.parent = parent
        super(pyinotify.ProcessEvent, self).__init__()

    def process_IN_MODIFY(self, e):
        if e.name == self.parent.config_basename:
            print("Config will be reloaded on next slide change...")
            # FIXME: We get a deadlock here sometimes. Possibly because the modify event triggers twice
            self.parent.lock.acquire()
            print("Reloading config...")
            self.parent.read_config()
            self.parent.lock.release()
        
class Config(QObject):

    refres = pyqtSignal()
    
    def __init__(self, f, handlers):
        QObject.__init__(self)
        self.configfile = f

        self.config_dict = {}
        self.slides = []
        self.resources = []

        self.handlers = handlers
        
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

        defaults = PropertyBag(self.config["defaults"])
        
        self.slides = []
        slides = self.config["slides"]

        for s in slides:
            if 'url' in s and not 'file' in s and not 'directory' in s:
                url = s['url']
                # FIXME: clone is ugly. Change to using a chain of
                # PropertyBags. That would also allow us to change
                # default settings globally
                props = defaults.clone()
                del s['url']
                props.update(s)
                self.resources.append(UrlResource(url, self.handlers,
                                                  properties = props))
            elif 'file' in s and not 'url' in s and not 'directory' in s:
                f = s['file']
                props = defaults.clone()
                del s['file']
                props.update(s)
                self.resources.append(FileResource(file, properties = props))
            elif 'directory' in s and not 'url' in s and not 'file' in s:
                d = s['directory']
                props = defaults.clone()
                del d['directory']
                props.update(s)
                self.resources.append(DirectoryResource(file, properties = props))
            
    
        # TODO: Rewrite parsing of config array completely. This organization doesn't make sense anymore
        self.slides = self.config["slides"]
        self.slides = [self._fill_defaults(el) for el in self.slides]       
        self.slides = sum([self._expand_directory(el) for el in self.slides], [])
        self.slides = sum([self._expand_path(el) for el in self.slides], [])
        #self.slides = sum([self._expand_rss for en in self.slides], [])
        self.slides = sum([[el]*el['frequency'] for el in self.slides], [])
        
        print(self.slides)
        
        if self.config["randomize"]:
            print("Randomizing")
            random.shuffle(self.slides)
        print(self.slides)

        self.reloaded = True
    
    def slidesgen(self):
        while True:
            for s in self.slides:
                self.lock.acquire()
                if self.reloaded:
                    self.reloaded = False
                    self.lock.release()
                    break
                yield s
                self.lock.release()
            if self.config["randomize"]:
                random.shuffle(self.slides)
                
    def _expand_path(self, el):
        if not "file" in el:
            return [el]
        el["file"] = os.path.join(self.config["basepath"], el["file"])
        if not os.path.exists(el["file"]):
            print("Warning: File", el["file"], "Doesn't exists")
            return []
        return [el]

    def _fill_defaults(self, el):
        for k in ["delay", "frequency", "caption"]:
            if not k in el:
                el[k] = self.config["defaults"][k]
        return el

    
    def end(self):
        self.notifier.stop()


