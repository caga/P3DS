import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff
from datetime import datetime, timedelta
from convertMd2Html import convertMd2Html
klasor="markdowns/"
class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified=datetime.now()
        self.convert=convertMd2Html(" "," ")
    def on_modified(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
        if not event.is_directory:
            modifiedFile=event.__repr__().split("'")[-2]
            fileFirstName=modifiedFile.split("/")[-1].split(".")[0]
            generatedHtml="web/"+fileFirstName+".html"
            print("* Modified File: %s" % modifiedFile)
            self.convert.inFile=modifiedFile
            self.convert.outFile=generatedHtml
            print("     -> Trying to generate modified html: %s " % generatedHtml)
            self.convert.convert2Html()
        # os.system("python createDesignDocs.py")
    def on_deleted(self,event):
        deletedFile=event.__repr__().split("'")[-2]
        fileFirstName=deletedFile.split("/")[-1].split(".")[0]
        deletedHtml="web/"+fileFirstName+".html"
        self.convert.inFile=deletedFile
        self.convert.outFile=deletedHtml
        print("* File deleted: %s" % deletedFile)
        print("     -> Trying to delete corresponding html file: %s" % deletedHtml)
        self.convert.deleteHtml()
    def on_created(self,event):
        createdFile=event.__repr__().split("'")[-2]
        fileFirstName=createdFile.split("/")[-1].split(".")[0]
        generatedHtml="web/"+fileFirstName+".html"
        print("* Created File: %s" % createdFile)
        # print("fileFirstName: %s" % fileFirstName)
        print("     -> Trying to generate html: %s " % generatedHtml)
        self.convert.inFile=createdFile
        self.convert.outFile=generatedHtml
        self.convert.convert2Html()
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
