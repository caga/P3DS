import dosya
import sys
from dosya import *
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta

import threading
from threading import Thread
class WatchHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_modified=datetime.now()
    def on_modified(self, event):
        print("modified:{}".format(event.__repr__()))
    def on_deleted(self,event):
        print("deleted: {}".format(event.__repr__()))
    def on_created(self,event):
        print("created: {}".format(event.__repr__()))
    def den(self,a):
        def alt(b):
           return b
        print ("alt fonksyon sonuc:{}".format(alt(a)))
class Watcher:
    def __init__(self,klasor:Klasor):
        self.watchHandler=WatchHandler()
        self.observer=None
        self.klasor=klasor
        self.thread=None 
        # self.watchHandler.den.alt():
            # print("aha")
    def watcher(self):
        self.observer=Observer()
        self.observer.schedule(self.watchHandler,path=str(self.klasor.path),recursive=False)
        self.observer.start()
        print("izleme başladı")
        sys.stderr.write("hede")
        sys.stdout.write("eauiea")
    def watcherStop(self):
        self.observer.stop()
        self.observer.join()
        print ("watcher is closed")
        print(self.observer.is_alive())

