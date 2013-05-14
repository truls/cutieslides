
from PyQt4.QtCore import *

from config import Config
from window import *
import mimetypes
import os.path
from threading import Lock, Thread
import time

IMAGE, VIDEO = range(2)

class Director(QThread):
    def __init__(self, control):
        super(QThread, self).__init__()

        self.control = control

    def run(self):
        while True:
            self.control.lock.acquire()
            print("Lock acquired")
            n  = next(self.control.slides)
            print(n)
            mtype = self.control._mimetype(n['file'])
            print(mtype)
            if mtype == IMAGE:
                self.control.change_slide.emit(n)
                time.sleep(n['delay'])
                try:
                    self.control.lock.release()
                except:
                    print("WARNING: Unable to release lock: syncronization issues")
                print("Lock released")
            elif mtype == VIDEO:
                self.control.change_slide.emit(n)
            else:
                self.control.lock.release()
                
                continue


class Control(QObject):
    change_slide = pyqtSignal(object)

    def __init__(self, window, config, parent = None):
        super(Control, self).__init__(parent)

        assert isinstance(config, Config)
        #assert isinstance(window, Main)
        
        self.config = config
        self.window = window

        self.slides = self.config.slidesgen()

        # Initialize mimetypes
        mimetypes.init()

        self.change_slide.connect(self.next_slide)
        self.window.video.finished.connect(self.video_finished)

        self.lock = Lock()


    def _mimetype(self, path):
        # FIMXE: Move MIME logic to somewhere else
        try:
            mimetype = mimetypes.types_map[os.path.splitext(path)[1]]
        except KeyError:
            print("Could not find mimetype for extension")
            return -1
            
        print("Found mimetype: ", mimetype)

        if "image/" in mimetype:
            return IMAGE
        elif "video/" in mimetype:
            return VIDEO
        else:
            print("Unknown mimetype")

    def start_show(self):
        self.thread.start()

    def next_slide(self, slide):

        n = slide
        print(n)
        
        mtype = self._mimetype(n['file'])
        
        if mtype == IMAGE:
            self.window.load_image(n['file'])
            self.window.show_image()
           # QTimer.singleShot(n['delay'] * 1000, self.video_finished)
        elif mtype == VIDEO:            
            vidobj = self.window.load_video(n['file'], self.video_finished)
            #vidobj.finished.connect(self.video_finished)

        self.window.set_caption(n['caption'])
              

    def video_finished(self):
        print("video_finished triggered")
        self.window.video.stop()
        self.lock.release()
        print("video finished")


