from dosya import *
import subprocess
import sys

class FileConverter:
    def __init__(self,inFile:Dosya,outFile:Dosya):
        self.inFile=inFile
        self.outFile=outFile
        self.errcode=0
    def convert2Html(self):
        errcode=subprocess.call(["pandoc", "-t", "html5", "--css","bulma.css",self.inFile.pathNFileName,"-s","-o",self.outFile.pathNFileName,"-M","title=Documentation Server","--filter","pandoc-plantuml"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if errcode !=0:
            print("         !!! Corresponding file '%s' can`t be generated. Error: %s" % (self.outFile, stderr))
        if errcode == 0:
            print("         :/ Html file generated: %s" % self.outFile)
    def deleteHtml(self):
        errcode=subprocess.call(["rm",self.outFile.pathNFileName],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if errcode !=0:
            print("         !!! Corresponding file '%s' can`t be deleted. Probably no such file exist!" % self.outFile)
        if errcode == 0:
            print("         :/ Corresponding File Deleted: %s" % self.outFile)
