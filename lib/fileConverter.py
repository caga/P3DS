from dosya import *
import subprocess
from subprocess import *
import sys
import os
from pandocfilters import *

class FileConverter:
    def __init__(self,inFile:Dosya,outFile:Dosya,imageFolder:Klasor):
        self.inFile=inFile.resolve()
        self.outFile=outFile.resolve()
        self.errcode=0
        self.imageFolder=imageFolder
    def convert2Html(self):
        process=None
        d=Dosya("cagaFilter.py")
        s="            filename = get_filename4code('{folder}', code)".format(folder=self.imageFolder / Path("Converted_Html"))
        d.satirDegistir("filename = get_filename4code",s)
        # process=subprocess.run(["pandoc", "-t", "html5", "--css","bulma.css",self.inFile,"-s","-o",self.outFile,"-M","title=Documentation Server","--filter","cagaFilter.py"],stdout=subprocess.PIPE,universal_newlines=True)
        process=subprocess.run(["pandoc","-s","--css","den.css",self.inFile,"-o",self.outFile,"--metadata", "pagetitle='Selam'","--filter","cagaFilter.py"],stdout=subprocess.PIPE,universal_newlines=True)              
        return process
    def convert2Pdf(self):
        process=None
        print("pdf` e cevirek")
        # print(str(self.outFile)[1:])
        d=Dosya("cagafilter_pdf.py")
        s="            filename = get_filename4code('{folder}', code)".format(folder=self.imageFolder / Path("Converted_Pdf"))
        d.satirDegistir("filename = get_filename4code",s)
        process=subprocess.run(["pandoc","-s","--css","den.css",self.inFile,"-o",self.outFile,"--metadata", "pagetitle='Selam'","--filter","cagafilter_pdf.py"],stdout=subprocess.PIPE,universal_newlines=True)              
        return process
