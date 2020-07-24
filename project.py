from lib.dosya import *
import lib.dosya
from lib.flaskServer import *
from flask_misaka import Misaka
from flask import *
import flask
import base64
import mimetypes
from lib.klasorWatch import *
from lib.fileConverter import *
import pdb

# import watchdog
# from Flask import send_static_file
a = None

class Den:
    def __init__(self):
        self.isim="cagatay"
class DocWathHandler(WatchHandler):
    def __init__(self,imageFolder:Klasor,html_outFolder:Klasor,pdf_outFolder:Klasor,converterCss:Dosya):
        super().__init__()
        self.html_outFolder=html_outFolder
        self.imageFolder=imageFolder
        self.pdf_outFolder=pdf_outFolder
        self.converterCss=converterCss
        self.last_modified=datetime.now()
    # def on_modified(self, event):
    #     print("ne haber")
    #     if datetime.now() - self.last_modified < timedelta(seconds=1):
    #         return
    #     else:
    #         self.last_modified = datetime.now()
    #     # print(event.event_type)
    #     print("modified:{}".format(event.__repr__()))
    #     inFile=Dosya(event.src_path)
    #     if not event.is_directory:
    #     # and (inFile.fileFirstName!="4913"): 
    #         print(inFile)
    #         print("Güncellenen markdown dosyası: {}".format(inFile))
    #         outFile= self.html_outFolder / (inFile.fileNameNoExt+".html") 
    #         converter=FileConverter(inFile,outFile,self.imageFolder,self.converterCss)
    #         converter.convert2Html()
    #         print("Tekrar oluşturulan html: {}".format(outFile))
    #         erasing_process=subprocess.run(["rm", (self.imageFolder / "Converted_Pdf-images/*"),"-fr"]) 
    #         print (erasing_process)
    #         outFile= self.pdf_outFolder / (inFile.fileNameNoExt+".pdf") 
    #         converter=FileConverter(inFile,outFile,self.imageFolder,self.converterCss)
    #         converter.convert2Pdf()
    #         print("Tekrar oluşturulan pdf: {}".format(outFile))
    #     else:
    #         return
    # def on_deleted(self,event):
    #     deletedFileMd=Dosya(event.src_path)
    #     if not event.is_directory and (deletedFileMd.fileFirstName!="4913"): 
    #         print("Silinen markdown dosyası: {}".format(deletedFileMd))
    #         CorrespondingHtml=self.html_outFolder / (deletedFileMd.fileNameNoExt+".html")
    #         CorrespondingPdf=self.pdf_outFolder / (deletedFileMd.fileNameNoExt+".pdf")
    #         try:
    #             erasing_html=subprocess.run(["rm", CorrespondingHtml])
    #             print("Otomatik Silinen html dosyası: {}".format(CorrespondingHtml))
    #             erasing_pdf=subprocess.run(["rm", CorrespondingPdf])
    #             print("Otomatik Silinen pdf dosyası: {}".format(CorrespondingPdf))
    #         except Exception as e:
    #             print(e)
    #     else:
    #        return 
        
    # def on_created(self,event):
    #     inFile=Dosya(event.src_path)
    #     if not event.is_directory and (inFile.fileFirstName!="4913"): 
    #         print("Yaratılan markdown dosyası: {}".format(inFile))
    #         outFile= self.html_outFolder / (inFile.fileNameNoExt+".html") 
    #         converter=FileConverter(inFile,outFile,self.imageFolder,self.converterCss)
    #         converter.convert2Html()
    #         print("Oluşturulan html: {}".format(outFile))
    #         erasing_process=subprocess.run(["rm", (self.imageFolder / "Converted_Pdf-images/*"),"-fr"]) 
    #         print (erasing_process)
    #         outFile= self.pdf_outFolder / (inFile.fileNameNoExt+".pdf") 
    #         converter=FileConverter(inFile,outFile,self.imageFolder,self.converterCss)
    #         converter.convert2Pdf()
    #         print("Oluşturulan pdf: {}".format(outFile))
    #     else:
    #        return 

class DocWatcher(Watcher):
    def __init__(self,klasor:Klasor,imageFolder:Klasor,outFolder:Klasor,pdf_outFolder:Klasor,converterCss:Dosya):
        Watcher.__init__(self,klasor)
        # super.__init__(self)
        self.watchHandler=DocWathHandler(imageFolder,outFolder,pdf_outFolder,converterCss)

class Project(Klasor):
    def __init__(self,level=None,):
        Klasor.__init__(self,level)
        self.web_klasor=Klasor(self / "webNdocs" )
        self.static_klasor=(self.web_klasor / "static")
        self.doc_klasor=(self.web_klasor / "docs")
        self.md_klasor=(self.doc_klasor / "markdowns")
        self.pdfDocs_outFolder=(self.doc_klasor / "pdfs")
        self.htmlDocs_outFolder=(self.doc_klasor / "htmls")
        self.converterCss=(self.static_klasor / "css/converter.css")
        self.src_klasor=[x for x in self.klasorler() if x.name=="src"][0]
        self.homePageImage=Dosya((self.static_klasor / "images"/ "baslik_it.jpg"))
        self.docImages=(self.static_klasor / "images")
        self.fs=None

        # self.DocWatcher=DocWatcher(self.md_klasor,self.static_klasor,self.htmlDocs_outFolder,self.pdfDocs_outFolder,self.converterCss)
        self.DocWatcher=DocWatcher(self.md_klasor,self.docImages,self.htmlDocs_outFolder,self.pdfDocs_outFolder,self.converterCss)

    def serverBuild(self,ip=None,port=None):
        if ip == None:
            if port == None:
                self.fs=FlaskServer(self.name,self.static_klasor,"127.0.0.1","5000")
                print(1)
            if port != None:
                self.fs=FlaskServer(self.name,self.static_klasor,"127.0.0.1",port)
                print(2)
        if ip != None:
            if port == None:
                self.fs=FlaskServer(self.name,self.static_klasor,ip,"5000")
                print(3)
            if port != None:
                self.fs=FlaskServer(self.name,self.static_klasor,ip,port)
                print(4)
        def home():
            global a
            mimetype="text/plain"
            d=self.homePageImage
            contex=d.oku2()
            contex=base64.b64encode(d.oku2()).decode("ascii")
            return render_template("ev.html",project=self,contex=contex)
        def fileShare(path):
            # pdb.set_trace()
            print(self)
            print(path)
            # path2file=self / filename
            dosya=Dosya(self / path)
            ftype=mimetypes.guess_type(dosya)
            if ftype[0].split("/")[1]=='pdf':
                contex=dosya.oku2()
                pdf=base64.b64encode(contex).decode("ascii")
                return render_template("ev.html",project=self,pdf=pdf)
            if ftype[0].split("/")[1]=='svg+xml':
                contex=dosya.oku2()
                svg=base64.b64encode(contex).decode('ascii')
                return render_template("ev.html",project=self,svg=svg)
            if ftype[0].split("/")[1]=='html':
                print("buraya girdikten sonra niye")
                print(dosya)
                # return send_file(dosya)
                contex=dosya.oku()
                return render_template("ev.html",project=self,html=contex)
            try:
                print("buraya devam ediyor?")
                context=dosya.oku()
                return render_template("ev.html",context=context,project=self)
            except UnicodeDecodeError:
                print("tanimlanmamıs binary file herhal!")
                contex=dosya.oku2()
                image=base64.b64encode(contex).decode("ascii")
                return render_template("ev.html",project=self,image=image)
        try:
            self.fs.add_endpoint(endpoint="/",endpoint_name="home",handler=home)
            self.fs.add_endpoint(endpoint="/dosyalar/{}/<path:path>".format(self),endpoint_name="fileShare",handler=fileShare)
        except Exception as e:
            print(e)
    def serverStart(self,ip=None,port=None):
        self.serverBuild(ip,port)
        self.fs.start()
        print("server ayakta mi: {}".format(self.fs.is_alive()))
    def serverStop(self):
        self.fs.stop()
        self.fs.join(timeout=3)
        print("server ayakta mi: {}".format(self.fs.is_alive()))
