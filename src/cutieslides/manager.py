
from PyQt4.QtCore import *

class Manager(QThread):
    
    def __init__(self, parent = None):
        super(QThread, self).__init__(parent)

    def handle_events(self):
        pass


