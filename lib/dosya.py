import glob
import os
import re
from pathlib import Path

s="."
treeString=""
treeCounter=0
silmessage=False
silinenObje=Path()
yaratmessage=False

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
        # self.pathNFileName.rename(s)
        self.__init__(s)
        print(self.fileName)
        # self.fileName=fileName
        # self.fileStrings=fileName.split(".")
        # self.SecondNameFlag=False
        # self.fileExtension=False
        # if len(self.fileStrings)==3:
        #     self.SecondNameFlag=True
        #     self.fileExtension=True
        #     self.fileFirstName=self.fileStrings[0]
        #     self.fileSecondName=self.fileStrings[1]
        #     self.fileExtension=self.fileStrings[2]
        # if len(self.fileStrings)==2:
        #     self.fileExtension=True
        #     self.fileFirstName=self.fileStrings[0]
        #     self.fileExtension=self.fileStrings[1]
        # if len(self.fileStrings)==1:
        #     self.fileFirstName=self.fileStrings[0]
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
            treeString=color.BOLD+treeString+self.name+color.END

        if self.__dosyaListesi !=[]:
            treeCounter=treeCounter+2
            for dosya in self.__dosyaListesi:
                treeString=treeString+"\n"+treeCounter*" "+"|__"+color.YELLOW+dosya.fileName+color.END
            treeCounter=treeCounter-2

        for altKlasor in self.__klasorListesi:
            treeCounter=treeCounter+2
            treeString=treeString+"\n"+treeCounter*" "+"|__"+color.BOLD+altKlasor.name+color.END
            altKlasor.__genTree()
            treeCounter=treeCounter-2
        #         # s=self.name+"\n|__"+color.BOLD+altKlasor.name+color.END
        #     if self.path.parent !=Path("."):
        #         s=s+"\n|   |_"+color.BOLD+altKlasor.name+color.END
        #         # s=s+"\n|_"+color.BOLD+altKlasor.name+color.END
        #         altKlasor.__genTree()
        #         if altKlasor.__dosyaListesi !=[]:
        #             for dosya in altKlasor.__dosyaListesi:
        #                 s=s+"\n    |_"+dosya.fileName
    def tree(self):
        self.__genTree()
        print(treeString)
        treeCounter=2

    def dosyaBul(self,fileName):
        path2File=Path()
        path2File=self.path / fileName
        p = [dosya for dosya in self.__dosyaListesi if path2File==dosya.pathNFileName][0]
        return p
        
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
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
