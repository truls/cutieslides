# -*- coding: utf-8 -*-

import sys
import signal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from window import *
from control import *
from config import Config


import time

main = None

def swap():
    print("Swapped image")
    main.show_image()

def play():
    print("Starting video")
    main.load_video(None)

if __name__ == "__main__":
    
    cf = Config("/home/truls/uni/kantine/slideshow/slides.yml")
    
    app = QApplication(sys.argv)

    main = Main()
    
    main.show()

    main.load_image(None)

    timer = QTimer()
    timer.setSingleShot(True)
    timer.setInterval(500)
    timer.timeout.connect(swap)
    timer.start()
    
    timer2 = QTimer()
    timer2.setSingleShot(True)
    timer2.setInterval(1500)
    timer2.timeout.connect(play)
    timer2.start()
    


    # Exit on Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
