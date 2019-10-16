#!/usr/bin/python
import re
import glob
import os
def degistir(basla,bitir,sayfa,veri):
    """TODO: Docstring for degistir.
    :returns: TODO
    """
    f=open(sayfa,"r+")
    lines=f.readlines()
    f.seek(0)
    wlines=[]
    c=0
    flag=False
    for line in lines:
        end=re.search(bitir,line)
        begin=re.search(basla,line)
        if begin:
            flag=True
            wlines.append(line)

        if end:
            flag=False
        if flag:
            if c<len(veri):
                wlines.append(veri[c])
            else:
                pass
            c+=1
        if not flag:
            wlines.append(line)
    f.seek(0)
    f.truncate()
    for line in wlines:
        f.write(line)
#iki satır arası okuma,,, henüz test edilmedi
def oku(basla,bitir,sayfa):
    f=open(sayfa,"r")
    lines=f.readlines()
    searchedPart=[]
    f.seek(0)
    c=0
    oku=False
    for line in lines:
        end=re.search(bitir,line)
        begin=re.search(basla,line)
        baslaSatiri=False
        if begin:
            oku=True
            baslaSatiri=True
        if end:
            oku=False
        if (oku and not baslaSatiri):
            searchedPart.append(line)
    return searchedPart
            


def silme():
    allFiles=set (glob.glob("*.*"))
    cssFiles=set (glob.glob("*.css"))
    jsFiles=set (glob.glob("*.js"))
    indexFile=set (glob.glob("index.html"))
    onyuzFiles=set(glob.glob("*.onyuz.html"))
    a=allFiles-indexFile
    b=a-cssFiles
    c=b-jsFiles
    beErased=c-onyuzFiles
    # print(beErased)
    for f in beErased:
        os.system("rm %s" % f)
# set olarak gönderiyor
def list(path,extension):
    pwd=os.getcwd()
    os.chdir(path)
    extensionFilter="*."+extension
    filelist=glob.glob(extensionFilter)
    return filelist

def namelist(path,extension):
    pwd=os.getcwd()
    os.chdir(path)
    extensionFilter="*."+extension
    namelist=set()
    filelist=glob.glob(extensionFilter)
    for file in filelist:
        fileFirstName=file.split(".")[0]
        namelist.add(fileFirstName)
    os.chdir(pwd)
    return set(namelist)
# uzantıları .html yapıp liste gönderiyor
def provisionalListWithHtmlExt(path,extension):
    pwd=os.getcwd()
    os.chdir(path)
    extensionFilter="*."+extension
    namelist=set()
    provisionalHtmlFiles=[]
    filelist=glob.glob(extensionFilter)
    for file in filelist:
        fileFirstName=file.split(".")[0]
        provisionalHtmlFile=fileFirstName+".html"
        provisionalHtmlFiles.append(provisionalHtmlFile)
    os.chdir(pwd)
    return provisionalHtmlFiles   

class Tekildosya:
    def __init__(self,fileName):
        self.fileStrings=fileName.split(".")
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
        print (self.fileStrings)
        print (len(self.fileStrings))
if "__main__"==__name__:
    print("Selam")
    f=input("dosya ismi-oku:")
    basla=input("baslangıç işaretçi:")
    bitir=input("son işaretçi: ")
    context=oku(basla,bitir,f)
    print(context)
