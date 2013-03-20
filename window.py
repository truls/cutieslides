# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import *

from control import NewSlideEvent

import time

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        
        # Holds current and next image widgets
        # load_image uses next
        self.current_image = None
        self.next_image = None
        self.current_pixmap = None
        self.next_pixmap = None
        self.current_video = None
        self.next_video = None
        self.current_mediasrc = None
        self.next_mediasrc = None

        self.screen_geom = QDesktopWidget().screenGeometry()
        
        pal = QPalette(self.palette())
        pal.setColor(QPalette.Window, Qt.black)
        pal.setColor(QPalette.WindowText, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        self.showFullScreen()
        
        self.image = QLabel(self)
        self.image.setGeometry(self.screen_geom)
        self.pixmap = QPixmap()
        self.pixmap.load("../../../Firefox_wallpaper.png")
        self.pixmap = self.pixmap.scaledToWidth(self.screen_geom.width())
        self.next_pixmap = QPixmap()
        
        print(self.frameSize().width())
        print(self.geometry())
        print(QDesktopWidget().screenGeometry())
        
        self.image.setPixmap(self.pixmap)
        self.image.show()

        self.video = Phonon.VideoPlayer(self)
        self.video.setGeometry(self.screen_geom)
        src = Phonon.MediaSource("../slides/slides/old/Torsdagssøster.m2t")
        self.video.load(src)
        self.video.finished.connect(self.video_done)
        self.video.hide()

        self.caption = QLabel(self)
        font = QFont()
        font.setPixelSize(20)
        self.caption.setFont(font)
        self.caption.setScaledContents(True)
        self.caption.setText("foobar bar baz barbar")
        self.caption.setGeometry(self.caption_target_geom(self.screen_geom))
        self.caption.show()


    def video_done(self):
        print("video done")

        sli
    def caption_target_geom(self, screen_geom):
        sw = screen_geom.width()
        sh = screen_geom.height()
        th = sw*0.10
        ret = QRect(0, sh - th, sw, th)
        print(ret)
        return ret

    def load_image(self, image):
        self.next_pixmap = QPixmap()
        self.next_pixmap.load("../../../Samba Top Can Bottle.JPG")
        self.next_pixmap = self.next_pixmap.scaledToWidth(self.screen_geom.width())
        print("loaded image")
    
    def show_image(self):
        self.pixmap.swap(self.next_pixmap)
        self.image.setPixmap(self.pixmap)
    
    def load_video(self, video):
        self.image.hide()
        self.video.show()
        self.video.play()
        self.caption.show()
        print(self.video.frameGeometry())
    
    def show_video(self):
        pass



