import sys
import signal
import time
import os.path

from downloader import Downloader, DownloadStatus, DownloadFailure, DownloadSuccess

from PyQt4.QtCore import QObject, pyqtSignal, QThreadPool
from PyQt4 import QtGui

from urllib.parse import urlparse
from handlers.redditrss import listimgs



class dltest(QObject):
    sign = pyqtSignal(object)

    def __init__(self, dl, feed):
        QObject.__init__(self)
        self.dl = dl
        self.feed = feed
    
    def test(self):
        self.sign.connect(self.dl_finished)

        for c, u in enumerate(listimgs(self.feed)):
            print("number", c)
            o = urlparse(u['url'])
            d = '/tmp/' + o.path[1:].replace("/", "-")
            print(d)
            self.dl.add(u['url'], d, self.sign)
        
        #self.dl.add('http://i.imgur.com/gAUVYEk.jpg', '/tmp/dl.test', self.sign)
        #print("exited")
        #self.dl.add('http://i.imgur.com/gAUVYEk.jpg', '/tmp/dl2.test', self.sign)
        #print("exited second")


    def dl_finished(self, ret):
        print(ret)
        print("done", self.feed)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dl = Downloader()
    a = dltest(dl, 'http://www.reddit.com/r/pics.rss')
    b = dltest(dl, 'http://www.reddit.com/r/itookapicture.rss')
    a.test()
    b.test()
    #dl.exit()
    print("exited")
    time.sleep(5)
    dl.active()
    #QThreadPool.globalInstance().waitForDone()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
    
