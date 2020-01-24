from dosya import *
import dosya
from flaskServer import *
from flask_misaka import Misaka
from flask import *
import flask
import base64
import mimetypes
from klasorWatch import *
from fileConverter import *
# import watchdog
# from Flask import send_static_file
a = None


class Den:
    def __init__(self):
        self.isim="cagatay"
class DocWathHandler(WatchHandler):
    def __init__(self,imageFolder:Klasor,outFolder:Klasor,pdf_outFolder:Klasor):
        super().__init__()
        self.outFolder=outFolder
        self.imageFolder=imageFolder
        self.pdf_outFolder=pdf_outFolder
    def on_modified(self, event):
        print("modified:{}".format(event.__repr__()))
        # inFile=Dosya(event.src_path)
        # outFile= self.outFolder / (inFile.fileNameNoExt+".html") 
        # converter=FileConverter(inFile,outFile,self.imageFolder)
        # converter.convert2Html()
    def on_deleted(self,event):
        print("deleted: {}".format(event.__repr__()))
    def on_created(self,event):
        print(event.src_path)
        inFile=Dosya(event.src_path)
        outFile= self.outFolder / (inFile.fileNameNoExt+".html") 
        converter=FileConverter(inFile,outFile,self.imageFolder)
        converter.convert2Html()
        outFile= self.pdf_outFolder / (inFile.fileNameNoExt+".pdf") 
        converter=FileConverter(inFile,outFile,self.imageFolder)
        converter.convert2Pdf()
        

class DocWatcher(Watcher):
    def __init__(self,klasor:Klasor,imageFolder:Klasor,outFolder:Klasor,pdf_outFolder:Klasor):
        Watcher.__init__(self,klasor)
        # super.__init__(self)
        self.watchHandler=DocWathHandler(imageFolder,outFolder,pdf_outFolder)

class Project(Klasor):
    def __init__(self,level=None,):
        Klasor.__init__(self,level)
        self.web_klasor=[x for x in self.klasorler() if x.name=="web"][0]
        self.src_klasor=[x for x in self.klasorler() if x.name=="src"][0]
        self.doc_klasor=[x for x in self.klasorler() if x.name=="docs"][0]
        self.md_klasor=[x for x in self.doc_klasor.klasorler() if x.name=="mdSource"][0]
        # self.docImages=[x for x in self.doc_klasor.klasorler() if x.name=="docImages"][0]
        self.docImages=[x for x in self.web_klasor.klasorler() if x.name=="static"][0]
        self.fs=None
        self.htmlDocs_outFolder=[x for x in self.doc_klasor.klasorler() if x.name=="htmls"][0]
        self.pdfDocs_outFolder=[x for x in self.doc_klasor.klasorler() if x.name=="pdfs"][0]

        # self.fs=FlaskServer(self.name,self.web_klasor)
        self.DocWatcher=DocWatcher(self.md_klasor,self.docImages,self.htmlDocs_outFolder,self.pdfDocs_outFolder)
    def serverBuild(self,ip=None,port=None):
        if ip == None:
            if port == None:
                self.fs=FlaskServer(self.name,self.web_klasor,"127.0.0.1","5000")
                print(1)
            if port != None:
                self.fs=FlaskServer(self.name,self.web_klasor,"127.0.0.1",port)
                print(2)
        if ip != None:
            if port == None:
                self.fs=FlaskServer(self.name,self.web_klasor,ip,"5000")
                print(3)
            if port != None:
                self.fs=FlaskServer(self.name,self.web_klasor,ip,port)
                print(4)
        self.fs.app.config["download"]="/home/osman/calismaAlani/P3DS/lib/DenemeProje/download"
        # dosyalar=Blueprint("dosyalar",__name__,static_folder=self.doc_klasor)
        # self.fs.app.register_blueprint(dosyalar,url_prefix="/dosyalar")
        # self.fs=FlaskServer(self.name,self.web_klasor,"172.26.140.25","5000")
        def home():
            global a
            mimetype="text/plain"
            # contex=send_from_directory(self.fs.app.config["download"],filename="den.txt",mimetype=mimetype,as_attachment=False)
            d=Dosya("./DenemeProje/web/static/images/baslik_it.jpg")
            contex=d.oku2()
            contex=base64.b64encode(d.oku2()).decode("ascii")
            # resp=send_from_directory("./DenemeProje/web/static/images","baslik_it.jpg")
            return render_template("ev.html",project=self,contex=contex)
        def about(**kwargs):
            for key,value in kwargs.items():
                print("%s == %s" %(key,value))
            return render_template("about.html")
        def mdden(user=None):
            d=Den()
            content="<h1> Selam </h1>"
            # path=self.md_klasor.path / Path("den.md")
            # with open(str(path),"r") as f:
                # content=f.read()
            return render_template('mdden.html', text=content,webklasor=self.web_klasor)
        def genel(sayfa=None):
            print(sayfa)
            return render_template("%s.html" % sayfa)
        # @self.fs.app.route("/den/<filename>")
        def deneme(filename):
            mimetype="text/plain"
            a= send_from_directory(self.fs.app.config["download"],filename=filename,mimetype=mimetype,as_attachment=False)
            return a
        def fileShare(path):
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
                contex=dosya.oku()
                return render_template("ev.html",project=self,html=contex)
            try:
                context=dosya.oku()
                return render_template("ev.html",context=context,project=self)
            except UnicodeDecodeError:
                print("tanimlanmamıs binary file herhal!")
                contex=dosya.oku2()
                image=base64.b64encode(contex).decode("ascii")
                return render_template("ev.html",project=self,image=image)
        try:
            self.fs.add_endpoint(endpoint="/",endpoint_name="home",handler=home)
            # self.fs.add_endpoint(endpoint="/about/<int:userid>",endpoint_name="about",handler=about)
            # self.fs.add_endpoint(endpoint="/mdden/<user>",endpoint_name="mdden",handler=mdden)
            # self.fs.add_endpoint(endpoint="/genel/<sayfa>",endpoint_name="genel",handler=genel)
            self.fs.add_endpoint(endpoint="/dosyalar/{}/<path:path>".format(self),endpoint_name="fileShare",handler=fileShare)
            # self.fs.app.add_url_rule("/den/<filename>","deneme",deneme)
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
