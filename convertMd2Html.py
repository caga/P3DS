#!/usr/bin/python
import os
import sys
import subprocess
class convertMd2Html:
    def __init__(self,inFile,outFile):
        self.inFile=inFile
        self.outFile=outFile
        self.errcode=0
    def convert2Html(self):
        errcode=subprocess.call(["pandoc", "-t", "html5", "--css","bulma.css",self.inFile,"-s","-o",self.outFile,"-M","title=Documentation Server","--filter","pandoc-plantuml"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if errcode !=0:
            print("         !!! Corresponding file '%s' can`t be generated. Error: %s" % (self.outFile, stderr))
        if errcode == 0:
            print("         :/ Html file generated: %s" % self.outFile)
        # os.system('pandoc -t html5 --css bulma.css %s -s -o %s --metadata pagetitle="Documentation Server" --filter pandoc-plantuml' % (self.inFile,self.outFile))
    def deleteHtml(self):
        errcode=subprocess.call(["rm",self.outFile],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            # os.system("rm %s" % self.outFile)
        if errcode !=0:
            print("         !!! Corresponding file '%s' can`t be deleted. Probably no such file exist!" % self.outFile)
        if errcode == 0:
            print("         :/ Corresponding File Deleted: %s" % self.outFile)
            # print("Hata: "+str(e))
            # pass

if __name__ == "__main__":
    if sys.argv[1]=="-h":
        print("Necessary argv: inFile,outFile")
    else:
        con=convertMd2Html(sys.argv[1],sys.argv[2])
        con.convert2Html()
