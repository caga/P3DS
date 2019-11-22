import glob
import os
import re
import threading
from threading import Thread
from concurrent.futures import Future
import http.server
import socketserver
from pathlib import *
import pathlib
import sys
# import colorama
# from colorama import Fore, Back, Style
# colorama.init()
s="."
treeString=""
webTree=""
treeCounter=2
silmessage=False
silinenObje=Path()
yaratmessage=False
STOPSERVER=False
dosyaBulundu=False
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

class Dosya(type(pathlib.Path())):
    def __init__(self,path):
        print(path)
        #super.__init__() çalışmıyor
        PosixPath.__init__(path)
        if isinstance(path,Path):
            s=str(path)
            PosixPath().__init__(s)
        else:
            PosixPath().__init__(path)

        self.fileName=str(path).split("/")[-1]
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
        s=self.replace(fileName)
        self.__init__(s)
        print(self.fileName)
    def sil(self):
        global silmessage
        global silinenObje
        # silmessage=self.path
        silmessage=True
        silinenObje=self
        self.unlink()
        returnString="silinen dosya: "+str(silinenObje)
        return returnString
    def yaz(self,String):
        self.write_text(String)
    def oku(self):
        return self.read_text()
        

    # def __str__(self):
    #     s=self.fileName
    #     return s
    # def __repr__(self):
    #     return "Dosya Nesnesi: {}".format(self.fileName)
class Klasor:
    def __init__(self,path,level=None):
        self.path=Path(path)
        self.level=level
        if level==None:
            self.level=0
        else:
            self.level=level
        self.name=self.path.parts[-1]
        self.__dosyaListesi=self.dosyalar(initial=True) 
        self.__klasorListesi=self.klasorler(initial=True)
        self.__dokumanListesi=self.dokumanlar(initial=True)
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
    def dokumanlar(self,initial=None):
        global silmessage
        global yaratmessage
        self.__dokumanListesi=[dosya for dosya in self.dosyalar(self) if dosya.fileExtension=="md"]
        return self.__dokumanListesi
    def klasorler(self,initial=None,level=None):
        global silmessage
        global yaratmessage
        if initial or silmessage or yaratmessage:
            self.__klasorListesi=[Klasor(str(altKlasor),self.level+1) for altKlasor in self.path.iterdir() if altKlasor.is_dir()]
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
        global webTree
        if self.path.parent ==Path("."):
            treeString=treeString+color.project+self.name+color.end
            webTree=webTree+self.name

        if self.__dosyaListesi !=[]:
            treeCounter=treeCounter+2
            for dosya in self.__dosyaListesi:
                treeString=treeString+"\n"+treeCounter*" "+"|__"+color.dosya+dosya.fileName+color.end
                webTree=webTree+"<pre>"+treeCounter*" "+"|__"+"<span style='color:blue'>"+dosya.fileName+"</span>"+"</pre>"
            treeCounter=treeCounter-2

        for altKlasor in self.__klasorListesi:
            treeCounter=treeCounter+2
            treeString=treeString+"\n"+treeCounter*" "+"|__"+color.directory+altKlasor.name+color.end
            webTree=webTree+"<pre>"+treeCounter*" "+"|__"+"<span style='color:red'>"+altKlasor.name+"</span>"+"</pre>"
            altKlasor.__genTree()
            treeCounter=treeCounter-2
    def tree(self):
        global treeString
        global webTree
        webTree=""
        self.__genTree()
        print(treeString)
        treeString=""
        treeCounter=0
    def wtree(self):
        global treeString
        global webTree
        webTree=""
        self.__genTree()
        toWeb=webTree
        treeString=""
        treeCounter=0
        return webTree
    def klasorBul(self,klasorName):
        pass



        
    def dosyaBul(self,fileName,level=None):
        if level==None:
            level=self.level
        def localBul(fileName):
            path2File=Path()
            path2File=self.path / fileName
            p = [dosya for dosya in self.__dosyaListesi if path2File==dosya.pathNFileName]
            if len(p)>0:
                return p[0]
            else:
                print("Klasor -> {} : file not found. Searching other subfolders".format(self.path))
                for klasor in self.klasorler():
                    p=klasor.dosyaBul(fileName,-1)
                    if p!=None:
                        return p
                        break
        p=localBul(fileName)
        if level>=0:
            if p!=None:
                print("\n \t File found: {}".format(p.pathNFileName))
            else:
                print("File not found")
        if p!=None:
            return p

    def klasorBul(self,klasorName,level=None):
        if level==None:
            level=self.level
        def localBul(klasorName):
            # path2File=Path()
            # path2File=self.path / fileName
            # p = [dosya for dosya in self.__dosyaListesi if path2File==dosya.pathNFileName]
            path2Klasor=Path()

            path2Klasor=self.path / klasorName
            p=[klasor for klasor in self.__klasorListesi if path2Klasor==klasor.path]
            if len(p)>0:
                return p[0]
            else:
                print("Klasor -> {} : Folder not found. Searching other subfolders".format(self.path))
                for klasor in self.klasorler():
                    p=klasor.klasorBul(klasorName,-1)
                    if p!=None:
                        return p
                        break
        p=localBul(klasorName)
        if level>=0:
            if p!=None:
                print("\n \t Folder found: {}".format(p.path))
            else:
                print("Folder not found")
        if p!=None:
            return p
        
        

    def sunucuBaslat(self,port):
        # global STOPSERVER
        # STOPSERVER = False
        self.port=port
        print(self.port)
        do_run=True
        self.thread=threading.Thread(target=self.server,daemon=True)
        self.thread.start()
            
        # docserve = threading.Thread(target=self.__server(port),daemon=True)
        # docserve.start()
        print("ERTAN")
        print (self.thread.isAlive())
    def sunucuKapat(self):
        self.thread.do_run=False
        # self.thread._tstate_lock.release_lock()
        self.thread._stop()
    def kontrol(self):
        print("thread:",self.thread.isAlive())

    def server(self):
        PORT = self.port
        direc=str(self.path)
        print("server başlayacak:",PORT)
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=direc, **kwargs)


        # Handler = http.server.SimpleHTTPRequestHandler
        # Handler.path=self.path
        # Handler.list_directory
        httpd = socketserver.TCPServer(("", PORT), Handler)
        print("Klasor Sunucusu %s Portunda başlatıldı" % PORT)
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
