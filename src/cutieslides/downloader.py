# Downloader

import urllib.request as url
import urllib.error as urlerr

from PyQt4.QtCore import QRunnable, QObject, QThreadPool, pyqtSignal

class DownloadStatus(object):
    pass
class DownloadFailure(DownloadStatus):
    pass
class DownloadSuccess(DownloadStatus):
    pass

class _Download(QRunnable):

    def __init__(self, src, dst, notify):
        super().__init__()
        self.src = src
        self.dst = dst
        self.notify = notify
        self.setAutoDelete(True)
    
    def run(self):
        try:
            f = url.urlopen(self.src)
        except urlerr.URLError:
            self.notify.emit(DownloadFailure)
            return
        if f is None:
            self.notify.emit(DownloadFailure)

        with open(self.dst, 'bw+') as fh:
            fh.write(f.read())
        
        self.notify.emit(DownloadSuccess)
        return
        

class Downloader(QObject):

    def __init__(self):
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(10)
        
    def add(self, src, dst, notify):
        self.pool.start(_Download(src, dst, notify))
        print("Added " + src)
        print(self.pool.activeThreadCount())

    def exit(self):
        print(self.pool.activeThreadCount())
        self.pool.waitForDone()

    def active(self):
        print(self.pool.activeThreadCount())
