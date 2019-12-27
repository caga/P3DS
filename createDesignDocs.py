import os
import glob
import re
import subprocess
import http.server
import socketserver
import dosya
#önce temizlik
os.chdir("web")
dosya.silme()
os.chdir("../")
# while (True):
#     print("web klasörünü temizleyelim mi? e/h")
#     x=input()
#     if x == "h":
#         break
#     if x == "e":
#         os.chdir("web")
#         dosya.silme()
#         os.chdir("../")
#         break
os.chdir("markdowns")
htmlIncludes=[]

#Dosyaları Ayarlayalım ve Htmle çevirelim

files=glob.glob("*.md")
for file in files:
    if os.getcwd().split("/")[-1]!="markdowns":
        os.chdir("../markdowns")
    fileFirstName=file.split(".")[0]
    htmlFileName=fileFirstName+".html"
    htmlInclude="<li><a href="+htmlFileName+">"+fileFirstName+"</a></li>\n"
    htmlIncludes.append(htmlInclude+"\n")
    os.chdir("../web")
    os.system('pandoc -t html5 --css bulma.css ../markdowns/%s -s -o %s --metadata pagetitle="Documentation Server" --filter pandoc-plantuml' % (file,htmlFileName))

# index.htmle dosyaları yazalım    
basla='<ul class="otomatik">'
bitir='</ul>'
sayfa="index.html"
dosya.degistir(basla,bitir,sayfa,htmlIncludes)

# # Server yapılandırması
# PORT = 8080
# Handler = http.server.SimpleHTTPRequestHandler
# httpd = socketserver.TCPServer(("", PORT), Handler)
# print("serving at port", PORT)
# httpd.serve_forever()
