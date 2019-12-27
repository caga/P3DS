from dosya import *
import dosya
from flaskServer import *
from flask_misaka import Misaka



class Den:
    def __init__(self):
        self.isim="cagatay"

class Project(Klasor):
    def __init__(self,level=None,):
        Klasor.__init__(self,level)
        self.web_klasor=[x for x in self.klasorler() if x.name=="web"][0]
        self.src_klasor=[x for x in self.klasorler() if x.name=="src"][0]
        # self.md_klasor=[x for x in self.web_klasor.klasorler() if x.name=="mdSource"][0]
        self.fs=None
        # self.fs=FlaskServer(self.name,self.web_klasor)

    def serverBuild(self,userid=None):
        self.fs=FlaskServer(self.name,self.web_klasor)
        def home():
            return render_template("ev.html")
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
            
            

        try:
            self.fs.add_endpoint(endpoint="/",endpoint_name="home",handler=home)
            self.fs.add_endpoint(endpoint="/about/<int:userid>",endpoint_name="about",handler=about)
            self.fs.add_endpoint(endpoint="/mdden/<user>",endpoint_name="mdden",handler=mdden)
            self.fs.add_endpoint(endpoint="/genel/<sayfa>",endpoint_name="genel",handler=genel)
        except Exception as e:
            print(e)
    def serverStart(self):
        self.serverBuild()
        self.fs.start()
        print("server ayakta mi: {}".format(self.fs.is_alive()))
    def serverStop(self):
        self.fs.stop()
        self.fs.join(timeout=3)
        print("server ayakta mi: {}".format(self.fs.is_alive()))






    # def createOrLoad(self,projectFolder):
        # self.parts=self.projectFolder.klasorler()
    # def createPart(self,part):
        # self.parts.append(part)
    # def deletePart(self,part):
        # path2Part=Path()
        # path2Part=self.project.path / part
   # def tree(self):
        # self.tree()
