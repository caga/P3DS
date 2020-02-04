from lib.dosya import *
import subprocess
from subprocess import *
import sys
import os
from pandocfilters import *
from pathlib import *

class FileConverter:
    def __init__(self,inFile:Dosya,outFile:Dosya,imageFolder:Klasor,cssFile:Dosya):
        self.inFile=inFile.resolve()
        self.outFile=outFile.resolve()
        self.errcode=0
        self.imageFolder=imageFolder
        self.cssFile=cssFile
        # self.cssFile=Dosya((outFile.parent / cssFile.name))
        # self.cssFile= Dosya(cssFile.name)
        # print("cssFile:{}".format(cssFile.name))
    def convert2Html(self):
        process=None
        # print(os.getcwd())
        d=Dosya("lib/cagaFilter.py")
        print(d)
        s="            filename = get_filename4code('{folder}', code)".format(folder=self.imageFolder / Path("Converted_Html"))
        d.satirDegistir("filename = get_filename4code",s)
        # process=subprocess.run(["pandoc", "-t", "html5", "--css",bulma.css",self.inFile,"-s","-o",self.outFile,"-M","title=Documentation Server","--filter","cagaFilter.py"],stdout=subprocess.PIPE,universal_newlines=True)
        process=subprocess.run(["pandoc","-s","--css","/"+str(self.cssFile),self.inFile,"-o",self.outFile,"--metadata", "pagetitle='Selam'","--filter","lib/cagaFilter.py"],stdout=subprocess.PIPE,universal_newlines=True)              
        return process
    def convert2Pdf(self):
        process=None
        print("pdf` e cevirek")
        # print(str(self.outFile)[1:])
        d=Dosya("lib/cagafilter_pdf.py")
        s="            filename = get_filename4code('{folder}', code)".format(folder=self.imageFolder / Path("Converted_Pdf"))
        d.satirDegistir("filename = get_filename4code",s)
        process=subprocess.run(["pandoc","-s","--css","-t","html5","/"+str(self.cssFile),self.inFile,"-o",self.outFile,"--metadata", "pagetitle='Selam'","--filter","lib/cagafilter_pdf.py"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)              
        return process
