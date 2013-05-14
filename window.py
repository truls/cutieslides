# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import *

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

        self.caption = QLabel(self)
        font = QFont()
        font.setPixelSize(20)
        self.caption.setFont(font)
        self.caption.setScaledContents(True)
        self.caption.setText("foobar bar baz barbar")
        self.caption.setGeometry(self.caption_target_geom(self.screen_geom))
        self.caption.show()

        # Move cursor out of the way
        QCursor().setPos(self.screen_geom.width(),
                         self.screen_geom.height())


    def caption_target_geom(self, screen_geom):
        sw = screen_geom.width()
        sh = screen_geom.height()
        th = sw*0.04
        ret = QRect(0, sh - th, sw, th)
        print("caption target geom", str(ret))
        return ret

    def load_image(self, image):
        self.next_pixmap = QPixmap()
        self.next_pixmap.load(image)
        self.next_pixmap = self.next_pixmap.scaled(self.screen_geom.size(),
                                                   aspectRatioMode = Qt.KeepAspectRatio)
        print("loaded image")
    
    def show_image(self):
        self.video.hide()
        print ("Show image")
        target_geom = QRect(int((self.screen_geom.width() / 2) -
                                self.next_pixmap.width() / 2),
                            int((self.screen_geom.height() / 2) -
                                (self.next_pixmap.height() / 2)),
                            self.next_pixmap.width(),
                            self.next_pixmap.height())
        
        self.pixmap.swap(self.next_pixmap)
        self.image.setPixmap(self.pixmap)
        self.image.setGeometry(target_geom)
        self.image.show()
        print ("Exit show image")
    
    def load_video(self, video, on_finish):
        if not self.current_video is None:
            # Orphan and dereference old video player
            # Adding too many video player widgets will fuck up
            # your program after a while
            self.current_video.parent.removeChild(self.current_video)
            del self.current_video

        vp = Phonon.VideoPlayer(self)
        vp.finished.connect(on_finish)
        # This will cause the video to autoscale nicely within the screen
        vp.setGeometry(self.screen_geom)
        src = Phonon.MediaSource(video)
        vp.load(src)
        vp.play()
        print("Before show: " + str(vp.sizeHint()))
        vp.show()
        print("After show: " + str(vp.sizeHint()))
        self.current_video = vp

    def set_caption(self, caption):
        self.caption.setText(caption)
    
    def show_video(self):
        pass



