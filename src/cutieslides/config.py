# -*- coding: utf-8 -*-

import pyinotify
import yaml
import os
import random
from threading import Lock

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

    def _expand_directory(self, el):
        if not "directory" in el:
            return [el]
        l = []
        d = el['directory']
        d_tmp = os.path.join(self.config['basepath'], d)
        try:
            dirlist = os.listdir(d_tmp)
            #print(d_tmp, dirlist)
        except OSError:
            # FIXME: Print contents of OSError exception
            print("Directory", d_tmp, "not found")
            return []
        for f in dirlist:
            nl = {'file': os.path.join(d, f),
                  'caption': el['caption'],
                  'delay': el['delay'],
                  'frequency': el['frequency']}
            l.append(nl)
        #print(l)
        return l
    
    def end(self):
        self.notifier.stop()


