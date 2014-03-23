# -*- coding: utf-8 -*-

import sys
import signal
import argparse
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from window import *
from control import *
from handler import Handler
from config import Config
from Downloader import Downloader


import time

main = None

def main():
    

    handler = Handler()
    downloader = Downloader()
    cf = Config("slides.yml", handler)
    
    app = QApplication(sys.argv)

    main = Main()
    control = Control(main, cf)
    director = Director(control)

    director.start()

    main.show()

    # Exit on Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
