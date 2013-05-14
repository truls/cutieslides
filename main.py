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

def main():
    
    cf = Config("slides.yml")
    
    app = QApplication(sys.argv)

    main = Main()
    control = Control(main, cf)
    director = Director(control)

    director.start()

    main.show()

    # Exit on Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
