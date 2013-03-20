
from PyQt4.QtCore import *

from config import Config
from window import *

class NewSlideEvent(QEvent):
    def __init__(self, slide, parent = None):
        pass

    def type(self):
        return 1000

    

class Control(QObject):
    
    def __init__(self, window, config, parent = None):
        assert isinstance(config, Config)
        assert isinstance(window, Window)
        
        self.config = config
        self.window = window

        self.next_slide = None

        self.timer = QTimer()
        self.timer.setSingleShot(True)
    
    def next_slide(self):
        slef.next_slide = self.config.next()
        n = self.config.next()
        if slidetype(n) is Video:
            self.switchvideo(next_slide)
        else:
            self.switchimage()

        self.timer.setInterval(n['interval'])
        self.timer.start()
        
    def event(self, event):
        super(QObject, self).event(event)

