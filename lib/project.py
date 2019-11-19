from dosya import *
import dosya
from flaskServer import *
from flask_misaka import Misaka



class Den:
    def __init__(self):
        self.isim="cagatay"

class Project(Klasor):
    def __init__(self,path,level=None,):
        Klasor.__init__(self,path,level)
        self.web_klasor=[x for x in self.klasorler() if x.name=="web"][0]
        self.src_klasor=[x for x in self.klasorler() if x.name=="src"][0]
        # self.md_klasor=[x for x in self.web_klasor.klasorler() if x.name=="mdSource"][0]
        self.fs=FlaskServer(self.name,self.web_klasor)
        Misaka(self.fs.app)

    def serverBuild(self,userid=None):
        def home():
            return render_template("home.html")
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


        self.fs.add_endpoint(endpoint="/",endpoint_name="home",handler=home)
        self.fs.add_endpoint(endpoint="/about/<int:userid>",endpoint_name="about",handler=about)
        self.fs.add_endpoint(endpoint="/mdden/<user>",endpoint_name="mdden",handler=mdden)
    def serverStart(self):
        self.serverBuild()
        self.fs.start()
    def serverStop(self):
        self.fs.stop()






    # def createOrLoad(self,projectFolder):
        # self.parts=self.projectFolder.klasorler()
    # def createPart(self,part):
        # self.parts.append(part)
    # def deletePart(self,part):
        # path2Part=Path()
        # path2Part=self.project.path / part
   # def tree(self):
        # self.tree()
