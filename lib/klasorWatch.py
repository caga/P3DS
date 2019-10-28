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
        print("modified")
    def on_deleted(self,event):
        print("deleted")
    def on_created(self,event):
        print("created")
class Watcher:
    def __init__(self,klasor):
        self.watchHandler=WatchHandler()
        self.observer=None
        self.klasor=Klasor(klasor)
        self.thread=None 
    # def kontrol(self):
        # print("thread:",self.thread.isAlive())
    # def start(self):
        # self.thread=threading.Thread(target=self.watcher,daemon=True)
        # self.thread.start()
    # def stop(self):
        # self.thread.do_run=False
    def watcher(self):
        self.observer=Observer()
        self.observer.schedule(self.watchHandler,path=str(self.klasor.path),recursive=False)
        self.observer.start()
        print("izleme başladı")
        sys.stderr.write("hede")
        sys.stdout.write("eauiea")
    def watcherStop(self):
        self.observer.stop()
        print ("watcher is closed")
        print(self.observer.is_alive())
        
# watcher=Watcher()
# observer.join()
# print("\n Documentation server is closed")
# print("\n Güle güle")
