import glob
import os
import re
import threading
from threading import Thread
from concurrent.futures import Future
import http.server
import socketserver
from pathlib import Path
import sys
# import colorama
# from colorama import Fore, Back, Style
# colorama.init()
s="."
treeString=""
treeCounter=2
silmessage=False
silinenObje=Path()
yaratmessage=False
STOPSERVER=False

# def call_with_future(fn, future, args, kwargs):
#     try:
#         result = fn(*args, **kwargs)
#         future.set_result(result)
#     except Exception as exc:
#         future.set_exception(exc)

# def threaded(fn):
#     def wrapper(*args, **kwargs):
#         future = Future()
#         Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
#         return future
#     return wrapper

class Dosya:
    def __init__(self,pathNFileName):
        self.pathNFileName=Path(pathNFileName)
        self.fileName=str(pathNFileName).split("/")[-1]
        self.fileStrings=self.fileName.split(".")
        self.SecondNameFlag=False
        self.fileExtension=False

        if len(self.fileStrings)==3:
            self.SecondNameFlag=True
            self.fileExtension=True
            self.fileFirstName=self.fileStrings[0]
            self.fileSecondName=self.fileStrings[1]
            self.fileExtension=self.fileStrings[2]
        if len(self.fileStrings)==2:
            self.fileExtension=True
            self.fileFirstName=self.fileStrings[0]
            self.fileExtension=self.fileStrings[1]
        if len(self.fileStrings)==1:
            self.fileFirstName=self.fileStrings[0]
    def isimDegistir(self,fileName):
        s=str(self.pathNFileName.parent)+"/"+fileName
        self.__init__(s)
        print(self.fileName)
    def sil(self):
        global silmessage
        global silinenObje
        # silmessage=self.pathNFileName
        silmessage=True
        silinenObje=self.pathNFileName
        self.pathNFileName.unlink()
        returnString="silinen dosya: "+str(silinenObje)
        return returnString
    def yaz(self,String):
        self.pathNFileName.write_text(String)
    def oku(self):
        return self.pathNFileName.read_text()
        

    def __str__(self):
        s=self.fileName
        return s
    def __repr__(self):
        return "Dosya Nesnesi: {}".format(self.fileName)
class Klasor:
    def __init__(self,path):
        self.path=Path(path)
        self.name=self.path.parts[-1]
        self.__dosyaListesi=self.dosyalar(initial=True) 
        self.__klasorListesi=self.klasorler(initial=True)
        self.pipein=os.pipe()
        self.pipeout=os.pipe()
        self.port=8000
        self.thread=None 
    def dosyalar(self,initial=None):
        global silmessage
        global silinenObje
        global yaratmessage
        dosyaListesi=[Dosya(dosya) for dosya in self.path.iterdir() if dosya.is_file()]
        if initial or silmessage or yaratmessage :
            self.__dosyaListesi=[Dosya(dosya) for dosya in self.path.iterdir() if dosya.is_file()]
            silmessage=False
            yaratmessage=False
        return self.__dosyaListesi
    def klasorler(self,initial=None):
        global silmessage
        global yaratmessage
        if initial or silmessage or yaratmessage:
            self.__klasorListesi=[Klasor(str(altKlasor)) for altKlasor in self.path.iterdir() if altKlasor.is_dir()]
            silmessage=False
            yaratmessage=False
        return self.__klasorListesi
    def dosyaSil(self,fileName):
        path2File=Path()
        path2File=self.path / fileName
        p = [dosya for dosya in self.__dosyaListesi if path2File==dosya.pathNFileName][0]
        p.sil()
    def dosyaYarat(self,fileName):
        global yaratmessage
        path2File=Path()
        path2File=self.path / fileName
        path2File.touch()
        yaratmessage=True
        
        # print(path2File)
        # print(path2File.exists())
    def klasorYarat(self,klasorName):
        global yaratmessage
        path2File=Path()
        path2File=self.path / klasorName
        path2File.mkdir()
        yaratmessage=True
    def klasoruSil(self):
        try:
            self.path.rmdir()
        except Exception as e:
            print(e)
    def altKlasorSil(self,klasorName):
        path2Klasor=Path()
        path2Klasor=self.path / klasorName
        p=None
        try:
            p=[klasor for klasor in self.__klasorListesi if path2Klasor==klasor.path][0]
        except Exception as e:
            print("No such folder")
        if p!=None:
            p.klasoruSil()
        else:
            print("Nothing done!")
    def __genTree(self):
        global treeString
        global treeCounter
        if self.path.parent ==Path("."):
            treeString=treeString+color.project+self.name+color.end

        if self.__dosyaListesi !=[]:
            treeCounter=treeCounter+2
            for dosya in self.__dosyaListesi:
                treeString=treeString+"\n"+treeCounter*" "+"|__"+color.dosya+dosya.fileName+color.end
            treeCounter=treeCounter-2

        for altKlasor in self.__klasorListesi:
            treeCounter=treeCounter+2
            treeString=treeString+"\n"+treeCounter*" "+"|__"+color.directory+altKlasor.name+color.end
            altKlasor.__genTree()
            treeCounter=treeCounter-2
    def tree(self):
        global treeString
        self.__genTree()
        print(treeString)
        treeString=""
        treeCounter=0
    def dosyaBul(self,fileName):
        path2File=Path()
        path2File=self.path / fileName
        p = [dosya for dosya in self.__dosyaListesi if path2File==dosya.pathNFileName][0]
        return p
    def sunucuBaslat(self,port):
        global STOPSERVER
        STOPSERVER = False
        self.port=port
        print(self.port)
        self.thread=threading.Thread(target=self.server,daemon=True)
        self.thread.start()
            
        # docserve = threading.Thread(target=self.__server(port),daemon=True)
        # docserve.start()
        print("ERTAN")
        print (self.thread.isAlive())
    def sunucuKapat(self):
        global STOPSERVER
        STOPSERVER=True
        self.thread.do_run=False
        self.thread.join()
        print (self.thread.isAlive())
        self.thread._stop()
        print(self.thread.join())
        print (self.thread.isAlive())
        self.thread.join()
    def kontrol(self):
        print("thread:",self.thread.isAlive())

    # @threaded
    def server(self):
        # t=threading.currentThread()
        # original=sys.stderr
        global STOPSERVER
        STOPSERVER = False
        PORT = self.port
        print("server başlayacak:",PORT)
        Handler = http.server.SimpleHTTPRequestHandler
        Handler.path=self.path
        httpd = socketserver.TCPServer(("", PORT), Handler)
        print("Klasor Sunucusu %s Portunda başlatıldı" % PORT)
        # pid=os.forkpty()
        # print("Fork PID:",pid)
        # while not STOPSERVER:
        while getattr(self.thread,"do_run",True):
            # sys.stderr=open("serverLogs.txt","a")
            try:
                httpd.handle_request()
            except:
                print("thread içinde hata")
                self.thread._stop()
                self.thread.exit()
            # sys.stderr=original
        print("kapadık")
        return 1
        # sys.stdout=original
        
    def __str__(self):
        global silmessage
        if silmessage:
            self.__init__()
            silmessage=False
        s="Klasor: {}\n dosyaListesi: {}\n klasorListesi: {}".format(self.path,self.__dosyaListesi,self.__klasorListesi)
        return s
    def __repr__(self):
        global silmessage
        if silmessage:
            self.__init__()
            silmessage=False
        return "Klasor Nesnesi: {}".format(self.name)
class color:
    project="\033[0;0;35m"
    directory="\033[0;0;33m"
    dosya="\033[0;0;34m"
    end='\033[0m'
