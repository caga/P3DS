import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
klasor="markdowns/"
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # print("Got it!")
        os.system("python createDesignDocs.py")
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path=klasor, recursive=False)
print("izlenecek klasör: %s\n izleme başlatılıyor..." % klasor)
observer.start()
print("izleme başlatıldı. o^o ")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
