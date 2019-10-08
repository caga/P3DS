#!/usr/bin/python
import glob
import os
import re

class dosya:
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


        
    
        
