from flask import Flask, render_template,Response,request
from flask import *
import flask
from lib.dosya import Klasor,Dosya
from werkzeug.serving import make_server
import threading
from threading import Thread


class EndpointAction(object):

    def __init__(self, action):
        self.action = action

# __call__  instance fonksyon olarak kullanıldığında çağrılır
    def __call__(self,**kwargs):
        # Perform the action
        answer = self.action(**kwargs)
        # Create the answer (bundle it in a correctly formatted HTTP answer)
        # self.response = flask.Response(answer, status=200, headers={})
        self.response=make_response(answer)
        # Send it
        return self.response

class FlaskServer(Thread):
    def __init__(self,name,webklasor:Klasor,ip,port):
        Thread.__init__(self)
        self.ip=ip
        self.port=port
        self.app=Flask(name,static_folder=str(webklasor)+"/static",template_folder=str(webklasor)+"/templates",static_url_path="/"+str(webklasor)+"/static")
        self.srv=make_server(ip,int(port),self.app)
        # self.ctx=app.app_context()
        # self.ctx.push()
        self.webklasor=webklasor
        self.app.debug=True
    def webpath(self):
        print(self.webklasor)
    def run(self):
        # log.info("starting server")
        print("starting server")
        self.srv.serve_forever()
        # self.app.run()
    def stop(self):
        self.srv.shutdown()
    

    # def add_all_endpoints(self):
        # Add root endpoint
        # self.add_endpoint(endpoint="/", endpoint_name="home", handler=self.home)

        # Add action endpoints
        # self.add_endpoint(endpoint="/about", endpoint_name="about", handler=self.about)
        # you can add more ... 

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler),methods=["POST","GET"]) 
        # self.app.add_url_rule(endpoint, endpoint_name, handler) 
        # You can also add options here : "... , methods=['POST'], ... "

    # ==================== ------ API Calls ------- ====================
    # def home(self,userid=None):
    #     # Dummy action
    #     userid=request.args.get("userid")
    #     print(userid)

    #     # return "action" # String that will be returned and display on the webpage
    #     return render_template("home.html")
    #     # Test it with curl 127.0.0.1:5000

    # def about(self):
    #     # Dummy action
    #     # return "add_X"
    #     return render_template("about.html")
    #     # Test it with curl 127.0.0.1:5000/add_X

class DocServer(Klasor):
        
    def __init__(self,path,level=None,appName=None,port=None):
        Klasor.__init__(self,path,level)
        self.app=None
        if appName!=None:
            self.app=Flask("DocumentServer")
    def server(self):
        try:
            app=Flask("ertan")

            @app.route('/')
            def home():
                return render_template("home.html")
            @app.route("/den/")
            def about():
                return render_template("about.html")
            
            app.run()
        except:
            return "Hata"

        # self.Klasor=Klasor(".")
        # if Klasor!=None:
            # self.Klasor=Klasor
        # self.klasor=klasor
